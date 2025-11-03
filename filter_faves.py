import sys
from urllib.parse import parse_qs

from pyinaturalist import INAT_BASE_URL

from faves import get_user_faves

if len(sys.argv) < 2:
    print("""
Usage:
          $ uv run filter_faves <user_id> [url_params]
Example:
          To browse iNaturalist observations favourited by benarmstrong of
          Animalia (taxon_id=1) observed in 2025:

          $ uv run filter_faves benarmstrong "taxon_id=1&year=2025"
""")
    exit()
user_id = sys.argv[1]
if len(sys.argv) == 3:
    params_str = sys.argv[2]
    params = parse_qs(params_str)
else:
    params = {}

place_id = 7095 # Crete, GR
faves = get_user_faves(user_id, **params)
if params:
    print(f"{len(faves)} faves by {user_id} found for {params_str}")
faves_ids = ','.join(str(fave.id) for fave in faves)
print(f'{INAT_BASE_URL}/observations?id={faves_ids}')
