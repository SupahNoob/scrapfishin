from typing import Dict, List

from pydantic import BaseModel, HttpUrl, validator


class LoweredStr(str):
    """
    Ensure database collation sanity by ignoring case.
    """
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v) -> str:
        try:
            s = v.lower()
        except AttributeError:
            raise TypeError(f'"{v}" is not of type str, got: {type(v)}')
        return cls(s)

    def __repr__(self):
        return f'LoweredStr({super().__repr__()})'


class Base(BaseModel):
    """
    Enable ORM Mode on all instances.

    Further reading:
      https://pydantic-docs.helpmanual.io/usage/models/#orm-mode-aka-arbitrary-class-instances
    """
    class Config:
        orm_mode = True


class Allergy(Base):
    allergen: LoweredStr


class Cuisine(Base):
    region: LoweredStr


class Tag(Base):
    descriptor: LoweredStr


class Utensil(Base):
    item: LoweredStr


class Ingredient(Base):
    food: LoweredStr
    amount: str

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


class Recipe(Base):
    source: str
    glamor_shot_url: HttpUrl
    title: str
    prep_time: int
    difficulty: LoweredStr
    tags: List[Tag]
    allergies: List[Allergy]
    feeds: int = 2
    ingredients: List[Ingredient]
    utensils: List[Utensil]
    instructions_url: HttpUrl
    nutrition: Dict[str, str]  # TODO: model for NutritionalFact (name, amount, unit) ?
    cuisines: List[Cuisine]

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
