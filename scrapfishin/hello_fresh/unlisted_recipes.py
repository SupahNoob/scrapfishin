from scrapfishin.schema import Recipe


_base = {
    'source': 'Hello Fresh',
    'prep_time': 5,
    'difficulty': 'level 1'
}

tuscan_heat_spice = Recipe.parse_obj({
    **_base,
    'title': 'Tuscan Heat Spice',
    'ingredients': [
        {'food': 'basil', 'amount': '4 tablespoon'},
        {'food': 'rosemary', 'amount': '2 tablespoon'},
        {'food': 'oregano', 'amount': '2 tablespoon'},
        {'food': 'garlic powder', 'amount': '2 tablespoon'},
        {'food': 'cayenne', 'amount': '1 tablespoon'},
        {'food': 'ground fennel', 'amount': '1 tablespoon'}
    ]
})

blackening_spice = Recipe.parse_obj({
    **_base,
    'title': 'Blackening Spice',
    'ingredients': [
        {'food': 'smoked paprika', 'amount': '3 tablespoon'},
        {'food': 'paprika', 'amount': '1.5 tablespoon'},
        {'food': 'onion powder', 'amount': '1.5 tablespoon'},
        {'food': 'garlic powder', 'amount': '1 tablespoon'},
        {'food': 'white pepper', 'amount': '0.5 tablespoon'},
        {'food': 'black pepper', 'amount': '0.5 tablespoon'},
        {'food': 'thyme', 'amount': '0.25 tablespoon'},
        {'food': 'oregano', 'amount': '0.25 tablespoon'},
        {'food': 'cayenne', 'amount': '0.125 tablespoon'}
    ]
})

_smoky_cinammon_paprika_spice = Recipe.parse_obj({
    **_base,
    'title': 'Smoky Cinnamon Paprika Spice',
    'ingredients': [
        {'food': 'ground cloves', 'amount': '1 tablespoon'},
        {'food': 'onion powder', 'amount': '8 tablespoon'},
        {'food': 'ground cinnamon', 'amount': '8 tablespoon'},
        {'food': 'smoked paprika', 'amount': '6 tablespoon'},
        {'food': 'mustard powder', 'amount': '16 tablespoon'},
        {'food': 'sweet paprika', 'amount': '24 tablespoon'},
        {'food': 'white granulated sugar', 'amount': '24 tablespoon'}
    ]
})

_fall_harvest_spice_blend = Recipe.parse_obj({
    **_base,
    'title': 'Fall Harvest Spice Blend',
    'ingredients': [
        {'food': 'thyme', 'amount': '3 tablespoon'},
        {'food': 'ground sage', 'amount': '3 tablespoon'},
        {'food': 'garlic powder', 'amount': '2 tablespoon'},
        {'food': 'onion powder', 'amount': '1 tablespoon'},
    ]
})

_southwest_spice_blend = Recipe.parse_obj({
    **_base,
    'title': 'Southwest Spice Blend',
    'ingredients': [
        {'food': 'garlic powder', 'amount': '4 tablespoon'},
        {'food': 'cumin', 'amount': '2 tablespoon'},
        {'food': 'chili powder', 'amount': '2 tablespoon'}
    ]
})

_tunisian_spice_blend = Recipe.parse_obj({
    **_base,
    'title': 'Tunisian Spice Blend',
    'ingredients': [
        {'food': 'ground caraway seed', 'amount': '4 tablespoon'},
        {'food': 'ground coriander', 'amount': '4 tablespoon'},
        {'food': 'smoked paprika', 'amount': '4 tablespoon'},
        {'food': 'turmeric', 'amount': '4 tablespoon'},
        {'food': 'chili powder', 'amount': '4 tablespoon'},
        {'food': 'garlic powder', 'amount': '4 tablespoon'},
        {'food': 'cayenne', 'amount': '1 tablespoon'},
        {'food': 'ground cinnamon', 'amount': '1 tablespoon'},
        {'food': 'black pepper', 'amount': '1 tablespoon'}
    ]
})

_steak_spice_blend = Recipe.parse_obj({
    **_base,
    'title': 'Steak Spice Blend',
    'ingredients': [
        {'food': 'red chili flake', 'amount': '1 tablespoon'},
        {'food': 'ground coriander seed', 'amount': '1 tablespoon'},
        {'food': 'ground dill seed', 'amount': '2 tablespoon'},
        {'food': 'ground mustard seed', 'amount': '3 tablespoon'},
        {'food': 'garlic powder', 'amount': '4 tablespoon'},
        {'food': 'black pepper', 'amount': '4 tablespoon'}
    ]
})

# TODO: further reading:
# https://www.reddit.com/r/hellofresh/comments/bawnby/hello_fresh_diy_spice_blends/
#
# SELECT i.food
#   FROM ingredient AS i
#  WHERE i.food LIKE '%spice%'
_mexican_spice_blend
