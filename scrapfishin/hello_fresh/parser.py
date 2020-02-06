import bs4


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
