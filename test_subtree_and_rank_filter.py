from pyinaturalist import ClientSession, iNatClient, make_tree, ROOT_TAXON_ID

inat = iNatClient()
life_list = inat.observations.life_list(user_id=545640, taxon_id=3) # benarmstrong
root_taxon_id = 71261 # Accipitriformes
subtree = (
    lambda t: True
    if root_taxon_id is None
    else root_taxon_id in [t.id] + [a.id for a in t.ancestors]
)
include = lambda t: subtree(t) and t.rank in ["genus"]
tree = make_tree(life_list.data, include_ranks=["genus"], root_id=71261)
hide_root = tree.id == ROOT_TAXON_ID
# All genera on life list
for taxon_count in tree.flatten(hide_root=hide_root):
    if include(taxon_count):
        print(taxon_count.name)
