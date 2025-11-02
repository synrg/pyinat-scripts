from bs4 import BeautifulSoup
from pyinaturalist.constants import INAT_BASE_URL
from pyinaturalist.models import Observation
from pyinaturalist.v2 import get_observations
from requests.sessions import Session

FAVES_BASE_URL = f'{INAT_BASE_URL}/faves'

session = Session()

def get_observations_page(url, page=1):
    """Return observation ids from an iNat page containing observations.
    
    Since some pages on iNat have no corresponding API endpoints,
    we use BeautifulSoup 4 to extra observations from the page
    from markup resembling:

        <div class='observation' id='observation-1234'>…</div>

    For example, /faves/{user_id} pages are structured this way.
    """
    obs_ids = []
    with session.get(url, params={'page': page}) as response:
        if response.status_code == 200:
            data = response.text
            doc = BeautifulSoup(data, "html.parser")
            obs_els = doc.select('div.observation')
            if len(obs_els) == 0:
                raise IndexError('No more pages')
            for obs_el in obs_els:
                obs_id = obs_el['id'].replace('observation-', '')
                obs_ids.append(obs_id)
        else:
            raise IndexError('Page not found')
    return obs_ids

def get_user_faves(user_id, **params):
    """Get observations that have been favourited by a user.
    
    This could take a while if you have a lot of favourites (a second
    or two per page of 100).

    You can specify any `params` that the `/v2/observations` endpoint
    accepts, e.g. `place_id=#` to filter favourites by a specific place.
    """
    page = 1
    obs_ids = []
    url = f'{FAVES_BASE_URL}/{user_id}'
    while page:
        try:
            obs_ids.extend(get_observations_page(url, page))
            page += 1
        except IndexError:
            page = 0

    faves = Observation.from_json_list(get_observations(id=obs_ids, **params, fields='all'))
    return faves
