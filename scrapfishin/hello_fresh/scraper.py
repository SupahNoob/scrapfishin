from typing import List
import concurrent.futures as fs
import functools as ft
import itertools as it
import logging
import time
import re

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import pydantic

from scrapfishin.hello_fresh.parser import (
    extract_separated_tags, parse_next_ingredient, parse_next_nutrient_value
)
from scrapfishin.hello_fresh.const import BASE_URL
from scrapfishin.schema import Recipe, IngredientAmount
from scrapfishin.http import Chrome


log = logging.getLogger(__name__)


# TODO
#
# Remove caching after we hit v1.0.0 - no need to cache in prod since each URL
# is unlikely to be called multiple times within a single run.
#
# We could make this faster with asyncio/concurrent.futures.. let's consider
# doing so and establishing a sane rate limit for the scraper.
#
# Finally, .datatize_recipe and .scrape should probably see some refactoring.
# .scrape is an integration method, so it makes sense for it to do a lot, but
# .datatize_recipe is a bit of scrape, a bit of parse.
#

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
    # TODO: utilize explicit wait.until() to minimize of time spent here..
    #   https://selenium-python.readthedocs.io/waits.html#explicit-waits
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
    opts = [
        '--ignore-certificate-errors',
        '--incognito',
        '--headless',
        'window-size=1920x1080'
    ]
    with Chrome(*opts) as driver:
        driver.get(f'{BASE_URL}/{slug}')

        with ActionChains(driver) as actions:
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
    opts = [
        '--ignore-certificate-errors',
        '--incognito',
        '--headless',
        'window-size=1920x1080'
    ]
    with Chrome(*opts) as driver:
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
    opts = [
        '--ignore-certificate-errors',
        '--incognito',
        '--headless',
        'window-size=1920x1080'
    ]
    with Chrome(*opts) as driver:
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

    # TODO consider adding a unit converter .. examples like below will cause
    # a lot of irregularities in the database, especially when combining
    # recipes into other forms (e.g. like a shopping list)
    #
    # 1 can of tomato sauce = 1 box = 13.76 ounce
    # 1 sprig of <herb> = 0.25 ounce
    # 1 bunch of <herb> = 2.00 ounce
    # 1 tablespoon = 3 teaspoon
    #
    data = {
        'source': 'Hello Fresh',
        'glamor_shot_url': soup.find('img', {'alt': title_tag.text})['src'],
        'title': f'{title_tag.text} {title_tag.find_next().text}',
        'prep_time': f'{prep_tag.find_next().text}',
        'difficulty': f'{diff_tag.find_next().text}',
        'tags': [{'descriptor': t} for t in extract_separated_tags(tags_tag, section='tag')],
        'allergies': [{'allergen': a} for a in extract_separated_tags(allergy_tag, section='allergen')],
        'ingredient_amounts': [
            {
                'ingredient': {'food': tag.find_next().text},
                'amount': tag.text.split(' ')[0],
                'measurement': {'unit': tag.text.split(' ')[1]}
            }
            for tag in parse_next_ingredient(ingredients_tag)
        ],
        'utensils': [{'item': u} for u in extract_separated_tags(utensil_tag, section='utensil')],
        'instructions_url': f'{BASE_URL}/{slug}' if steps_tag is None else steps_tag['href'],
        'nutrition': {
            tag.text.lower(): tag.find_next().text
            for tag in parse_next_nutrient_value(nutrition_tag)
        }
    }

    return data


def scrape(scrapers: int=10) -> List[Recipe]:
    """
    Run through Hello Fresh collecting Recipes.

    This method will take a considerable amount of time to run as it is
    scraping almost every recipe listed on Hello Fresh.

    Parameters
    ----------
    scrapers : int, default 10
        number of workers concurrently scraping

    Returns
    -------
    recipes : list
        all known recipes on Hello Fresh
    """
    from scrapfishin.hello_fresh.unlisted_recipes import spices

    recipes  = [*spices]
    cuisines = {}

    # Aggregate all cuisine slugs into a single dict with the form..
    #
    # e.g.
    # {
    #     'italian': [
    #         '/recipe/delicious-soup-meal',
    #         ...
    #     ],
    #     ...
    # }
    #
    with fs.ThreadPoolExecutor(max_workers=scrapers) as ex:
        for slug in get_world_cuisines():
            cuisine = re.search(r'.*\/(.*)-.*', slug).group(1)
            cuisines[cuisine] = ex.submit(get_recipes, slug[1:])

        log.info(f'scraping {len(cuisines)} cuisines for recipe locations')
        fs.wait(cuisines.values())

    cuisines = {
        cuisine: future.result()
        for cuisine, future in cuisines.copy().items()
        if future.done() and not future.cancelled()
    }

    # Aggregate all Recipes into a single list with the form..
    #
    # e.g.
    # [
    #     {
    #         'source': 'Hello Fresh',
    #         ...
    #         'cuisines': [
    #             {'region': 'italian'},
    #         ]
    #     },
    #     ...
    # ]
    #
    with fs.ThreadPoolExecutor(max_workers=scrapers) as ex:
        for cuisine, slugs in cuisines.copy().items():
            futures = [ex.submit(datatize_recipe, slug[1:]) for slug in slugs]
            cuisines[cuisine] = futures

        log.info(f'scraping {len(futures)} recipe pages for data')
        fs.wait([fut for futures in cuisines.values() for fut in futures])

    recipe_data = [
        {**future.result(), **{'cuisines': [{'region': cuisine}]}}
        for cuisine, futures in cuisines.items()
        for future in futures
        if future.done() and not future.cancelled() and future.exception() is None
    ]

    # TODO
    #  in order to get useful information out of our errors, we need to wrap
    #  .datatize_recipe() with something that will catch and push the errors
    #  up in a ScrapError.
    #
    #  TBD..
    #
    #  class ScrapError(Exception):
    #      def __init__(self, e, slug):
    #          self.e = e
    #          self.slug = slug
    #
    #      # AttributeError - missing data on page
    #      # IndexError - malformed ingredient on page
    #      # pydantic.ValidationError - data doesn't pass validation
    #
    # errors = [
    #     for cuisine, futures in cuisines.items()
    #     for future in futures
    #     if future.exception() is not None
    # ]

    # Now, if recipes appear in multiple cuisine regions, we'll have duplicates
    # which will scare the database. Let's eliminate those dupes and append
    # recipe schema objects for return.
    #
    # Note: We'll also handle the Parent recipe relationship here.
    log.info(f'deduplicating and validating recipe data')
    for title, group in it.groupby(recipe_data, key=lambda r: r['title']):
        group = list(group)
        regions = {c['region'] for recipe in group for c in recipe['cuisines']}

        data = {
            **group[0],
            **{'cuisines': [{'region': region} for region in regions]},
            # OK YEAH I KNOW IT'S UGLY.
            #
            #   We essentially redefine the Ingredient in IngredientAmount if
            #   and only if a spice exists with the same name as the
            #   ingredient.
            #
            #   next(..., None) acts like dict().get('key', None)
            #
            **{
                'ingredient_amounts': [
                    IngredientAmount.parse_obj({
                        **i,
                        'ingredient': {
                            **i['ingredient'],
                            'parent_recipe': next(filter(lambda s: s.title.lower() == i['ingredient']['food'].lower(), spices), None)
                        }
                    })
                    for i in group[0]['ingredient_amounts']
                ]
            }
        }
        recipes.append(Recipe.parse_obj(data))

    return recipes
