from pyinaturalist import INAT_BASE_URL

from faves import get_user_faves

user_id = "dgcurrywheel"
place_id = 7095 # Crete, GR
faves = get_user_faves(user_id, place_id=place_id)
faves_ids = ','.join(str(fave.id) for fave in faves)
print(f"faves by {user_id} found for place_id={place_id}:")
print(f'{INAT_BASE_URL}/observations?id={faves_ids}')
