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
                raise StopIteration('Ran out of pages')
            for obs_el in obs_els:
                obs_id = obs_el['id'].replace('observation-', '')
                obs_ids.append(obs_id)
        else:
            raise StopIteration(f'Response status code = {response.status_code}')
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
        except StopIteration:
            page = 0
    print(f'{len(obs_ids)} faves by {user_id} found')
    page = 1
    faves = []
    while True:
        response = get_observations(id=obs_ids, per_page=200, page=page, **params, fields='all')
        _faves = Observation.from_json_list(response)
        if len(_faves) == 0:
            break
        else:
            faves.extend(_faves)
            page += 1

    return faves
