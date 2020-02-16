## Documentation

- for main GitHub page
- for Project
- for each Scraper

## Tests

1. Unit
  - e.g. City Bureau's [city scrapers][1]
2. Integration
  - test process of scraping a single recipe for each provider backend

## Images

- Scrap - the raccoon who fishes

## API

- Reconcile difference between Schema and Model

- ### Design

```python
from scrapfishin.schema import Recipe
from scrapfishin import Scrap

# Scrap object acts as connector to our database, but also as an entry
# point into the application. If no SQlAlchemy engine is provided, then
# a default SQLite database will be created in the temp directory.
scrap = Scrap()

# .fish()
#   this is our scraping endpoint. a limited set of arguments are
#   available to configure the scraping speed and number of recipes to
#   return.
scrap.fish(site='Hello Fresh')
scrap.fish(site='Blue Apron')
scrap.fish(site='Home Chef')

# .prepare()
#   can take a number of arguments and return 1+ recipes. The default
#   naked call will return 1 random recipe from the database, however
#   many options may be set:
#
#   title - a specific recipe to return
#   cuisine - all recipes must be of this specific type of cuisine
#   ingredients - all recipes must include these ingredients
#   website - return recipes from this specific provider
#   n - the number of recipes to return
r = scrap.prepare()
isinstance(r, Recipe)  # True

# .display() --> opens webpage
```

- ### Scrapers
  - Blue Apron
  - Hello Chef
  
  
[1]: https://github.com/City-Bureau/city-scrapers/tree/master/tests/files