from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey, Integer, Numeric, String
# import sqlalchemy as sa

from scrapfishin.database import Base


_rel_kw = {
    'cascade': 'all',
    'passive_deletes': True
}

_fk_kw = {
    'ondelete': 'CASCADE'
}


class PrettyModelMixin:
    """
    A mixin class for prettifying Model objects.
    """
    def __repr__(self):
        return f'<[dbo.{self.__tablename__}]>'


class Recipe(Base, PrettyModelMixin):
    """
    """
    __tablename__ = 'recipe'

    id = Column(Integer, primary_key=True)
    title = Column(String, unique=True)
    prep_time = Column(Integer, comment='in seconds')
    difficulty = Column(String)
    source = Column(String, comment='source can be a website, friend, etc')
    glamor_shot_url = Column(String)
    instructions_url = Column(String)

    allergies = relationship('Allergy', secondary='recipe_allergy', backref='recipes', **_rel_kw)
    cuisines = relationship('Cuisine', secondary='recipe_cuisine', backref='recipes', **_rel_kw)
    tags = relationship('Tag', secondary='recipe_tag', backref='recipes', **_rel_kw)
    utensils = relationship('Utensil', secondary='recipe_utensil', backref='recipes', **_rel_kw)
    ingredients = relationship('RecipeIngredientAmount', back_populates='recipe', **_rel_kw)
    # instructions
    # nutritional_facts

    def __repr__(self):
        return f'<[dbo.{self.__tablename__} ID={self.id}]>'


class Allergy(Base, PrettyModelMixin):
    """
    """
    __tablename__ = 'allergy'

    id = Column(Integer, primary_key=True)
    allergen = Column(String, unique=True)


class Cuisine(Base, PrettyModelMixin):
    """
    """
    __tablename__ = 'cuisine'

    id = Column(Integer, primary_key=True)
    region = Column(String, unique=True)


class Tag(Base, PrettyModelMixin):
    """
    """
    __tablename__ = 'tag'

    id = Column(Integer, primary_key=True)
    descriptor = Column(String, unique=True)


class Utensil(Base, PrettyModelMixin):
    """
    """
    __tablename__ = 'utensil'

    id = Column(Integer, primary_key=True)
    item = Column(String, unique=True)


class Ingredient(Base, PrettyModelMixin):
    """
    """
    __tablename__ = 'ingredient'

    id = Column(Integer, primary_key=True)
    food = Column(String, unique=True)
    parent_recipe_id = Column(Integer, ForeignKey('recipe.id'), nullable=True)

    recipes = relationship('RecipeIngredientAmount', back_populates='ingredient', **_rel_kw)


class Measurement(Base, PrettyModelMixin):
    """
    """
    __tablename__ = 'measurement'

    id = Column(Integer, primary_key=True)
    unit = Column(String, unique=True)


#
# Associations
#

class RecipeIngredientAmount(Base, PrettyModelMixin):

    __tablename__ = 'recipe_ingredient_amount'

    recipe_id = Column(Integer, ForeignKey('recipe.id', **_fk_kw), primary_key=True)
    ingredient_id = Column(Integer, ForeignKey('ingredient.id', **_fk_kw), primary_key=True)
    measurement_id = Column(Integer, ForeignKey('measurement.id', **_fk_kw))
    amount = Column(Numeric(10, 2, asdecimal=False))

    ingredient = relationship('Ingredient', back_populates='recipes')
    recipe = relationship('Recipe', back_populates='ingredients')


class RecipeAllergy(Base, PrettyModelMixin):
    """
    """
    __tablename__ = 'recipe_allergy'

    recipe_id = Column(Integer, ForeignKey('recipe.id', **_fk_kw), primary_key=True)
    allergy_id = Column(Integer, ForeignKey('allergy.id', **_fk_kw), primary_key=True)


class RecipeCuisine(Base, PrettyModelMixin):
    """
    """
    __tablename__ = 'recipe_cuisine'

    recipe_id = Column(Integer, ForeignKey('recipe.id', **_fk_kw), primary_key=True)
    cuisine_id = Column(Integer, ForeignKey('cuisine.id', **_fk_kw), primary_key=True)


class RecipeTag(Base, PrettyModelMixin):
    """
    """
    __tablename__ = 'recipe_tag'

    recipe_id = Column(Integer, ForeignKey('recipe.id', **_fk_kw), primary_key=True)
    tag_id = Column(Integer, ForeignKey('tag.id', **_fk_kw), primary_key=True)


class RecipeUtensil(Base, PrettyModelMixin):
    """
    """
    __tablename__ = 'recipe_utensil'

    recipe_id = Column(Integer, ForeignKey('recipe.id', **_fk_kw), primary_key=True)
    utensil_id = Column(Integer, ForeignKey('utensil.id', **_fk_kw), primary_key=True)
