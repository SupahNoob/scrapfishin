from ward import test, fixture
from bs4 import BeautifulSoup

from scrapfishin.scrapers.hello_fresh import extract_tags


@fixture
def tag():
    html = """
    <div class="dsan dsab dsao dsap dsaq dsh dsar dsas dsat dsau dsax dsay dsaz dsba dsdb dsda dsdc">
     <span class="dsa dsb dsc dscm dse dsde">
      <span data-translation-id="recipe-detail.allergens">
       Allergens
      </span>
      :
     </span>
     <span class="dsa dsb dsc dsd">
      <span class="">
       <span class="fela-_36rlri">
        Wheat
       </span>
       <span class="fela-_36rlri">
        <span class="fela-_13jy121">
         •
        </span>
        Eggs
       </span>
       <span class="fela-_36rlri">
        <span class="fela-_13jy121">
         •
        </span>
        Milk
       </span>
      </span>
     </span>
    </div>
    """
    return BeautifulSoup(html, 'html.parser')


@test('extract_tags returns at least an empty list')
def _(tags_tag=tag):
    t = extract_tags(tags_tag)
    print(type(t))
    assert isinstance(t, list)
