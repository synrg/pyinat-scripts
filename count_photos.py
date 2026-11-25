from pyinaturalist import get_observations
USERNAME='benarmstrong'
response = get_observations(user_id=USERNAME, page='all')
results = response["results"]
print(f'{USERNAME} has {sum(len(obs["photos"]) for obs in results)} photos and {len(results)} observations')
