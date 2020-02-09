from typing import Iterable

import sqlalchemy as sa

from scrapfishin.models import Recipe


def grocery_list(
    s: sa.orm.Session,
    recipes: Iterable[Recipe]
) -> str:
    """
    Format an iterable of Recipes into a Grocery List.

    Parameters
    ----------
    s : sqlalchemy.orm.Session
        database session to bind objects

    recipes : [Recipe]
        list of recipes to shop for

    Returns
    -------
    grocery_page : str
        page of sorted ingredients
    """
    seen = []

    for r in recipes:
        for i in r.ingredient_amounts:
            unit = f'{i.measurement.unit} of {i.ingredient.food}'
            amount = i.amount

            try:
                existing = next(s for s in seen if unit in s)
            except StopIteration:
                pass
            else:
                amount += float(existing.split(' ')[0])
                seen.remove(existing)

            seen.append(f'{amount} {unit}')

    return '\n'.join(sorted(seen, key=lambda i: i.split(' of ')[-1]))
