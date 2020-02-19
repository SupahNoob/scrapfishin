from scrapfishin.schema import Recipe


_base = {
    'source': 'Hello Fresh',
    'prep_time': 10,
    'difficulty': 'level 1',
    'tags': [{'descriptor': 'spice mix'}]
}

tuscan_heat_spice = Recipe.parse_obj({
    **_base,
    'title': 'Tuscan Heat Spice',
    'ingredient_amounts': [
        {'ingredient': {'food': 'basil'}, 'amount': '4', 'measurement': {'unit': 'teaspoon'}},
        {'ingredient': {'food': 'rosemary'}, 'amount': '2', 'measurement': {'unit': 'teaspoon'}},
        {'ingredient': {'food': 'oregano'}, 'amount': '2', 'measurement': {'unit': 'teaspoon'}},
        {'ingredient': {'food': 'garlic powder'}, 'amount': '2', 'measurement': {'unit': 'teaspoon'}},
        {'ingredient': {'food': 'cayenne'}, 'amount': '1', 'measurement': {'unit': 'teaspoon'}},
        {'ingredient': {'food': 'ground fennel'}, 'amount': '1', 'measurement': {'unit': 'teaspoon'}}
    ]
})

blackening_spice = Recipe.parse_obj({
    **_base,
    'title': 'Blackening Spice',
    'ingredient_amounts': [
        {'ingredient': {'food': 'smoked paprika'}, 'amount': '3', 'measurement': {'unit': 'teaspoon'}},
        {'ingredient': {'food': 'paprika'}, 'amount': '1.5', 'measurement': {'unit': 'teaspoon'}},
        {'ingredient': {'food': 'onion powder'}, 'amount': '1.5', 'measurement': {'unit': 'teaspoon'}},
        {'ingredient': {'food': 'garlic powder'}, 'amount': '1', 'measurement': {'unit': 'teaspoon'}},
        {'ingredient': {'food': 'white pepper'}, 'amount': '0.5', 'measurement': {'unit': 'teaspoon'}},
        {'ingredient': {'food': 'black pepper'}, 'amount': '0.5', 'measurement': {'unit': 'teaspoon'}},
        {'ingredient': {'food': 'thyme'}, 'amount': '0.25', 'measurement': {'unit': 'teaspoon'}},
        {'ingredient': {'food': 'oregano'}, 'amount': '0.25', 'measurement': {'unit': 'teaspoon'}},
        {'ingredient': {'food': 'cayenne'}, 'amount': '0.125', 'measurement': {'unit': 'teaspoon'}}
    ]
})

smoky_cinammon_paprika_spice = Recipe.parse_obj({
    **_base,
    'title': 'Smoky Cinnamon Paprika Spice',
    'ingredient_amounts': [
        {'ingredient': {'food': 'ground cloves'}, 'amount': '1', 'measurement': {'unit': 'teaspoon'}},
        {'ingredient': {'food': 'onion powder'}, 'amount': '8', 'measurement': {'unit': 'teaspoon'}},
        {'ingredient': {'food': 'ground cinnamon'}, 'amount': '8', 'measurement': {'unit': 'teaspoon'}},
        {'ingredient': {'food': 'smoked paprika'}, 'amount': '6', 'measurement': {'unit': 'teaspoon'}},
        {'ingredient': {'food': 'mustard powder'}, 'amount': '16', 'measurement': {'unit': 'teaspoon'}},
        {'ingredient': {'food': 'sweet paprika'}, 'amount': '24', 'measurement': {'unit': 'teaspoon'}},
        {'ingredient': {'food': 'white granulated sugar'}, 'amount': '24', 'measurement': {'unit': 'teaspoon'}}
    ]
})

fall_harvest_spice_blend = Recipe.parse_obj({
    **_base,
    'title': 'Fall Harvest Spice Blend',
    'ingredient_amounts': [
        {'ingredient': {'food': 'thyme'}, 'amount': '3', 'measurement': {'unit': 'teaspoon'}},
        {'ingredient': {'food': 'ground sage'}, 'amount': '3', 'measurement': {'unit': 'teaspoon'}},
        {'ingredient': {'food': 'garlic powder'}, 'amount': '2', 'measurement': {'unit': 'teaspoon'}},
        {'ingredient': {'food': 'onion powder'}, 'amount': '1', 'measurement': {'unit': 'teaspoon'}},
    ]
})

southwest_spice_blend = Recipe.parse_obj({
    **_base,
    'title': 'Southwest Spice Blend',
    'ingredient_amounts': [
        {'ingredient': {'food': 'garlic powder'}, 'amount': '4', 'measurement': {'unit': 'teaspoon'}},
        {'ingredient': {'food': 'cumin'}, 'amount': '2', 'measurement': {'unit': 'teaspoon'}},
        {'ingredient': {'food': 'chili powder'}, 'amount': '2', 'measurement': {'unit': 'teaspoon'}}
    ]
})

tunisian_spice_blend = Recipe.parse_obj({
    **_base,
    'title': 'Tunisian Spice Blend',
    'ingredient_amounts': [
        {'ingredient': {'food': 'ground caraway seed'}, 'amount': '4', 'measurement': {'unit': 'teaspoon'}},
        {'ingredient': {'food': 'ground coriander'}, 'amount': '4', 'measurement': {'unit': 'teaspoon'}},
        {'ingredient': {'food': 'smoked paprika'}, 'amount': '4', 'measurement': {'unit': 'teaspoon'}},
        {'ingredient': {'food': 'turmeric'}, 'amount': '4', 'measurement': {'unit': 'teaspoon'}},
        {'ingredient': {'food': 'chili powder'}, 'amount': '4', 'measurement': {'unit': 'teaspoon'}},
        {'ingredient': {'food': 'garlic powder'}, 'amount': '4', 'measurement': {'unit': 'teaspoon'}},
        {'ingredient': {'food': 'cayenne'}, 'amount': '1', 'measurement': {'unit': 'teaspoon'}},
        {'ingredient': {'food': 'ground cinnamon'}, 'amount': '1', 'measurement': {'unit': 'teaspoon'}},
        {'ingredient': {'food': 'black pepper'}, 'amount': '1', 'measurement': {'unit': 'teaspoon'}}
    ]
})

steak_spice_blend = Recipe.parse_obj({
    **_base,
    'title': 'Steak Spice Blend',
    'ingredient_amounts': [
        {'ingredient': {'food': 'red chili flake'}, 'amount': '1', 'measurement': {'unit': 'teaspoon'}},
        {'ingredient': {'food': 'ground coriander seed'}, 'amount': '1', 'measurement': {'unit': 'teaspoon'}},
        {'ingredient': {'food': 'ground dill seed'}, 'amount': '2', 'measurement': {'unit': 'teaspoon'}},
        {'ingredient': {'food': 'ground mustard seed'}, 'amount': '3', 'measurement': {'unit': 'teaspoon'}},
        {'ingredient': {'food': 'garlic powder'}, 'amount': '4', 'measurement': {'unit': 'teaspoon'}},
        {'ingredient': {'food': 'black pepper'}, 'amount': '4', 'measurement': {'unit': 'teaspoon'}}
    ]
})

mexican_spice_blend = Recipe.parse_obj({
    **_base,
    'title': 'Mexican Spice Blend',
    'ingredient_amounts': [
        {'ingredient': {'food': 'chili powder'}, 'amount': '6', 'measurement': {'unit': 'teaspoon'}},
        {'ingredient': {'food': 'cumin'}, 'amount': '3', 'measurement': {'unit': 'teaspoon'}},
        {'ingredient': {'food': 'salt'}, 'amount': '1.5', 'measurement': {'unit': 'teaspoon'}},
        {'ingredient': {'food': 'ground black pepper'}, 'amount': '1.5', 'measurement': {'unit': 'teaspoon'}},
        {'ingredient': {'food': 'paprika'}, 'amount': '1', 'measurement': {'unit': 'teaspoon'}},
        {'ingredient': {'food': 'red pepper flakes'}, 'amount': '0.5', 'measurement': {'unit': 'teaspoon'}},
        {'ingredient': {'food': 'oregano'}, 'amount': '0.5', 'measurement': {'unit': 'teaspoon'}},
        {'ingredient': {'food': 'garlic powder'}, 'amount': '0.5', 'measurement': {'unit': 'teaspoon'}},
        {'ingredient': {'food': 'onion powder'}, 'amount': '0.5', 'measurement': {'unit': 'teaspoon'}},
        {'ingredient': {'food': 'ground cayenne pepper'}, 'amount': '0.25', 'measurement': {'unit': 'teaspoon'}}
    ]
})

zaatar_spice_blend = Recipe.parse_obj({
    **_base,
    'title': 'Za\'atar Spice Blend',
    'ingredient_amounts': [
        {'ingredient': {'food': 'toasted sesame seeds'}, 'amount': '3', 'measurement': {'unit': 'teaspoon'}},
        {'ingredient': {'food': 'salt'}, 'amount': '0.5', 'measurement': {'unit': 'teaspoon'}},
        {'ingredient': {'food': 'ground'}, 'amount': 'cumin 0.5', 'measurement': {'unit': 'teaspoon'}},
        {'ingredient': {'food': 'dried'}, 'amount': 'thyme 3', 'measurement': {'unit': 'teaspoon'}},
        {'ingredient': {'food': 'oregano'}, 'amount': '3', 'measurement': {'unit': 'teaspoon'}},
        {'ingredient': {'food': 'marjoram'}, 'amount': '3', 'measurement': {'unit': 'teaspoon'}},
        {'ingredient': {'food': 'sumac'}, 'amount': '9', 'measurement': {'unit': 'teaspoon'}}
    ]
})

# TODO: further reading:
# https://www.reddit.com/r/hellofresh/comments/bawnby/hello_fresh_diy_spice_blends/
#
# SELECT i.ingredient
#   FROM ingredient AS i
#  WHERE i.ingredient LIKE '%spice%'
#
# mediterranean spice blend
# ranch spice
# fajita spice blend
# enchilada spice blend
# taco spice blend
# cajun spice blend

spices = [
    tuscan_heat_spice,
    blackening_spice,
    smoky_cinammon_paprika_spice,
    fall_harvest_spice_blend,
    southwest_spice_blend,
    tunisian_spice_blend,
    steak_spice_blend,
    mexican_spice_blend,
    zaatar_spice_blend
]
