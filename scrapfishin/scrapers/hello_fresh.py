from typing import List
import functools as ft
import logging
import time
import re

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import pydantic
import bs4

from scrapfishin.schema import Recipe
from scrapfishin.http import Chrome

# TODO: ... refactor each provider into their own directory
#
# /scrapfishin
# └─ /hello_fresh
#    ├─ __init__.py          (things that are common immutables like BASE_URL)
#    ├─ scraper.py
#    ├─ parser.py
#    └─ unlisted_recipes.py  (mostly spice blends)
#

BASE_URL = 'https://www.hellofresh.com'
log = logging.getLogger(__name__)


def handle_promo_popup(actions: ActionChains) -> None:
    """
    Ignores the Hello Fresh marketing bullshit. :)

    As of time of writing (2020/01/01), if Hello Fresh recognizes you
    are not logged into the website, it will prompt the viewer with a
    promotional offer. We'll just send an ESCAPE and move along.

    Parameters
    ----------
    actions : ActionChains
        object used to automate low level interactions
    """
    time.sleep(7)
    actions.send_keys(Keys.ESCAPE).perform()
    time.sleep(1)


@ft.lru_cache()
def get_world_cuisines(slug: str='recipes') -> List[str]:
    """
    Scrape all the links in the "world cuisines" category.

    Utilizes the main recipes page to obtain all of the "World Cuisines"
    category. https://www.hellofresh.com/recipes/ and scroll down to the
    section labeled "World cuisines" - you'll find a carousel of sorts.

    Parameters
    ----------
    slug : str
        resource of the recipes archive

    Returns
    -------
    cuisine_links : List[str]
        a list of all world cuisines pages
    """
    with Chrome('--ignore-certificate-errors', '--incognito') as driver:
        with ActionChains(driver) as actions:
            driver.get(f'{BASE_URL}/{slug}')
            handle_promo_popup(actions)

            # scroll down, allowing the loading of Javascript which generates
            # the "World cuisines" section
            actions.send_keys(Keys.PAGE_DOWN).perform()
            time.sleep(2)

            # hit the bottom of the page for good measure
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            time.sleep(1)

        soup = BeautifulSoup(driver.page_source, 'html.parser')

    links = soup.find_all('a', href=True)
    return [a['href'] for a in links if '-cuisine' in a['href']]


@ft.lru_cache()
def get_recipes(slug: str) -> List[str]:
    """
    Scrape all the links for recipes listed on <slug>.

    Loads the resource at <slug> and finds the button to "LOAD MORE"
    recipes. Once finished loading all recipes in the part of the
    archive, aggregates all links on the page and returns them.

    Parameters
    ----------
    slug : str
        resource of the page aggregating recipes

    Returns
    -------
    recipe_links : List[str]
        a list of all recipes found on a page
    """
    with Chrome('--ignore-certificate-errors', '--incognito') as driver:
        with ActionChains(driver) as actions:
            driver.get(f'{BASE_URL}/{slug}')
            handle_promo_popup(actions)

            # continue loading recipes until they are no more to load
            try:
                while True:
                    driver.find_element_by_partial_link_text('LOAD MORE').click()
                    time.sleep(3)
            except NoSuchElementException:
                pass

        soup = BeautifulSoup(driver.page_source, 'html.parser')

    food_images = soup.find_all('img', {'data-test-id': 'recipe-image'})
    return list(set([img.find_previous('a')['href'] for img in food_images]))


def parse_next_ingredient(tag: bs4.Tag) -> bs4.Tag:
    """
    Traverse the DOM to find the next ingredient Tag.

    Parameters
    ----------
    tag : bs4.Tag
        container tag for the Ingredients section

    Yields
    ------
    ingredient : bs4.Tag
        tag of the next ingredient in the section

    Returns
    -------
    None
    """
    while True:
        tag = tag.find_next()

        if tag.text == 'Not included in your delivery':
            return

        if tag.name != 'img':
            continue

        yield tag.find_next().find_next()


def parse_next_nutrient_value(tag: bs4.Tag) -> bs4.Tag:
    """
    Traverse the DOM to find the next nutrient Tag.

    Parameters
    ----------
    tag : bs4.Tag
        container tag for the Nutrion Values section

    Yields
    ------
    value : bs4.Tag
        tag of the next value in the section

    Returns
    -------
    None
    """
    while True:
        tag = tag.find_next()

        if tag.text.startswith('Due to the different suppliers'):
            return

        if tag.name != 'span':
            continue

        if tag.text.endswith('depending on your region.'):
            continue

        if any(_ in tag.text.lower() for _ in ['nutri', 'serving', 'arrow']):
            continue

        # we arrive at a Nutritional Fact (e.g. Calories, Fat, Protein, ...)
        # the next Tag will be its value, so the two tags together would
        # express something like "Protein 40 g"
        yield tag

        # this is why we toss in a secondary find_next, before hitting the next
        # loop iteration
        tag = tag.find_next()

#
#
#


def extract_separated_tags(tag: bs4.element.Tag, *, section) -> list:
    """
    Pull a list of tags from the DOM.

    The "Tags" and "Allergens" DOM wrappers have the same exact
    formatting.

    Parameters
    ----------
    tag : bs4.element.Tag
        identifier tag for the section of a recipe

    Returns
    -------
    tags : list
        list of tags, possibly empty
    """
    tags = []

    if tag is None:
        return tags

    if section in ['tag', 'allergen']:
        tags = tag.find_next().text.split('•')

    if section == 'utensil':
        tags = tag.find_next('span', text='•').parent.parent.text.split('•')[1:]

    return list(set(tags))


@ft.lru_cache()
def datatize_recipe(slug: str) -> dict:
    """
    Parse the Recipe page DOM into a JSON response.

    Parameters
    ----------
    slug : str
        resource of the recipe page

    Returns
    -------
    recipe : Recipe
    """
    with Chrome('--ignore-certificate-errors', '--incognito') as driver:
        with ActionChains(driver) as actions:
            driver.get(f'{BASE_URL}/{slug}')
            handle_promo_popup(actions)

        soup = BeautifulSoup(driver.page_source, 'html.parser')

    title_tag   = soup.find('h1',   {'data-test-id': 'recipeDetailFragment.recipe-name'})
    prep_tag    = soup.find('span', {'data-translation-id': 'recipe-detail.preparation-time'})
    diff_tag    = soup.find('span', {'data-translation-id': 'recipe-detail.cooking-difficulty'})
    tags_tag    = soup.find('span', {'data-translation-id': 'recipe-detail.tags'})
    allergy_tag = soup.find('span', {'data-translation-id': 'recipe-detail.allergens'})
    ingredients_tag = soup.find('span', {'data-translation-id': 'recipe-detail.ingredients'})
    utensil_tag = soup.find('span', {'data-translation-id': 'recipe-detail.utensils'})
    steps_tag   = soup.find('a', {'data-test-id': 'recipeDetailFragment.instructions.downloadLink'})
    nutrition_tag   = soup.find('div', {'data-test-id': 'recipeDetailFragment.nutrition-values'})

    data = {
        'source': 'Hello Fresh',
        'glamor_shot_url': soup.find('img', {'alt': title_tag.text})['src'],
        'title': f'{title_tag.text} {title_tag.find_next().text}',
        'prep_time': f'{prep_tag.find_next().text}',
        'difficulty': f'{diff_tag.find_next().text}',
        'tags': [{'descriptor': t} for t in extract_separated_tags(tags_tag, section='tag')],
        'allergies': [{'allergen': a} for a in extract_separated_tags(allergy_tag, section='allergen')],
        'ingredients': [
            {
                'food': tag.find_next().text,
                'amount': tag.text
            }
            for tag in parse_next_ingredient(ingredients_tag)
        ],
        'utensils': [{'item': u} for u in extract_separated_tags(utensil_tag, section='utensil')],
        'instructions_url': steps_tag['href'],
        'nutrition': {
            tag.text.lower(): tag.find_next().text
            for tag in parse_next_nutrient_value(nutrition_tag)
        }
    }

    return data


def scrape() -> list:
    """
    Run through the website
    """
    recipes = []

    for world_slug in get_world_cuisines():
        cuisine = re.search('.*\/(.*)-.*', world_slug).group(1)
        log.info(f'scraping {cuisine.title()} recipes')

        for i, recipe_slug in enumerate(get_recipes(world_slug[1:]), start=1):
            try:
                r = datatize_recipe(recipe_slug[1:])
                r['cuisines'] = [{'region': cuisine}]

                try:
                    existing = next((_ for _ in recipes if _.title == r['title']))
                except StopIteration:
                    pass
                else:
                    recipes.remove(existing)
                    r['cuisines'].extend([c.dict() for c in existing.dict()['cuisines']])

                print(r)
                r = Recipe(**r)
                recipes.append(r)
            except pydantic.ValidationError as e:
                log.error(f'url: {recipe_slug}\n{e}')
            except AttributeError as e:
                log.error(f'missing data on page: {recipe_slug} {e}')
        
            if len(recipes) > 2:
                return recipes

    log.info(f'{len(recipes)} recipes found!')
    return recipes
