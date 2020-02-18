from typing import List
import tempfile
import pathlib

from scrapfishin.database import Database, Base
from scrapfishin.schema import Recipe, Ingredient
from scrapfishin import hello_fresh


class Scrap:
    """
    Scrap the hungry bandit!

    This is the main entrypoint into the scrapfishin library. TODO

    Attributes
    ----------
    conn_str : str, default 'sqlite:///{some_temp_dir}/scrapfishin.db'
        SQLAlchemy URL that points to your database
    """
    def __init__(self, conn_str: str=None):
        if conn_str is None:
            temp_dir = pathlib.Path(tempfile.gettempdir()) / 'scrapfishin'
            temp_dir.mkdir(parents=True, exist_ok=True)
            temp_dir = temp_dir.resolve().as_posix()
            conn_str = f'sqlite:///{temp_dir}/scrapfishin.db'

        self.db = Database(conn_str)
        Base.metadata.create_all(self.db.engine)

    def fish(self, site: str, *, persist: bool=True) -> List[Recipe]:
        """
        TODO
        """
        supported = {
            'hello fresh': hello_fresh,
            # 'blue apron': blue_apron,
            # 'home chef': home_chef
        }

        try:
            lib = supported[site.lower()]
        except KeyError:
            raise ValueError(f'"{site}" is not a supported')

        recipes = lib.scrape()

        if persist:
            raise NotImplementedError('TODO: persist relational structure to database')

        return recipes

    def prepare(self, *, cuisine=None, n=1):
        """
        """
        NotImplementedError('TODO: tons of options on this one...')

    def collect(self, recipes: List[Recipe], follow_parents: bool=False) -> List[Ingredient]:
        """
        Reduce a list of recipes to their ingredients.

        Parameters
        ----------
        recipes : List[Recipe]
            recipe objects to consolidate

        follow_parents : bool, default False
            whether or not to reduce Ingredients if they have a parent recipe

        Returns
        -------
        ingredients : List[Ingredient]
        """
        ingredients = [i for r in recipes for i in r.ingredients]

        if follow_parents:
            raise NotImplementedError('TODO: add logic to find parent recipes')

        return ingredients
