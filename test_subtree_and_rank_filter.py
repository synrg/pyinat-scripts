# Example use of make_tree and a custom include to filter
# specific ranks within a life list subtree.
from pyinaturalist import iNatClient, make_tree, ROOT_TAXON_ID

inat = iNatClient()

# Whole life list
user_id = 545640 # benarmstrong
taxon_id = 3 # birds
life_list = inat.observations.life_list(user_id=user_id, taxon_id=taxon_id)

# Subtree of life list
root_taxon_id = 71261 # Accipitriformes
include_ranks = ["genus"]

subtree = (
    lambda t: True
    if root_taxon_id is None
    else root_taxon_id in [t.id] + [a.id for a in t.ancestors]
)
include = lambda t: subtree(t) and t.rank in include_ranks
tree = make_tree(life_list.data, include_ranks=include_ranks, root_id=root_taxon_id)
hide_root = tree.id == ROOT_TAXON_ID

# All genera in life list subtree
for taxon_count in tree.flatten(hide_root=hide_root):
    if include(taxon_count):
        print(taxon_count.name)
