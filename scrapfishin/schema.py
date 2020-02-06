from typing import Union, Dict, List

from pydantic import BaseModel, HttpUrl, validator


class OrmModeModel(BaseModel):

    class Config:
        orm_mode = True


class Allergy(OrmModeModel):
    allergen: str

    @validator('allergen')
    def str_lower(cls, v) -> str:
        """
        Ensure database sanity by ignoring case.
        """
        return v.lower()


class Cuisine(OrmModeModel):
    region: str

    @validator('region')
    def str_lower(cls, v) -> str:
        """
        Ensure database sanity by ignoring case.
        """
        return v.lower()


class Tag(OrmModeModel):
    descriptor: str

    @validator('descriptor')
    def str_lower(cls, v) -> str:
        """
        Ensure database sanity by ignoring case.
        """
        return v.lower()


class Utensil(OrmModeModel):
    item: str

    @validator('item')
    def str_lower(cls, v) -> str:
        """
        Ensure database sanity by ignoring case.
        """
        return v.lower()


class Ingredient(OrmModeModel):
    food: str
    amount: str

    @validator('food')
    def str_lower(cls, v) -> str:
        """
        Ensure database sanity by ignoring case.
        """
        return v.lower()

    @validator('amount', pre=True)
    def unicode_replace(cls, v) -> str:
        """
        Replaces unicode reprs with their float amount.

            ¼ = 0.25
            ⅓ = 0.33
            ½ = 0.50
            ¾ = 0.75
        """
        mapping = {
            '\u00bc': '.25',
            '\u2153': '.33',
            '\u00bd': '.50',
            '\u00be': '.75'
        }

        for unicode_, fraction in mapping.items():
            v = v.replace(unicode_, fraction)

        return v


class Recipe(OrmModeModel):
    source: str
    glamor_shot_url: HttpUrl
    title: str
    prep_time: int
    difficulty: str
    tags: List[Tag]
    allergies: List[Allergy]
    ingredients: List[Ingredient]
    utensils: List[Utensil]
    instructions_url: HttpUrl
    nutrition: Dict[str, str]       # TODO: model for NutritionalFact (name, amount, unit) ?
    cuisines: List[Cuisine]
    # TODO: feeds: int = 2   # the amount of people the recipe is designed for

    @validator('difficulty')
    def str_lower(cls, v) -> str:
        """
        Ensure database sanity by ignoring case.
        """
        return v.lower()

    @validator('prep_time', pre=True)
    def hours_to_minutes(cls, v) -> int:
        """
        Normalize all time units.
        """
        if isinstance(v, int):
            return v

        amount, denom = v.split(' ')
        minutes = int(amount)

        if denom == 'hours':
            minutes *= 60

        return minutes
