from collections import Counter
from infomap import Infomap

import matplotlib.pyplot as plt
import numpy as np
import json

from spotigraph.apicall import get_artist
from spotigraph.explore import get_first_gen, get_second_gen, get_user_library
from spotigraph.network import build_links, export_to_pajek, to_integer_indexed_graph
from spotigraph.types import Artist


artist_id = "15uNxh8omvRvH71kcdIe2r"
# artist_id = "1HY2Jd0NmPuamShAr6KMms"

seed_artist = get_artist(artist_id)
print(seed_artist)

graph_nodes = get_first_gen(artist_id)

first_gen = {artist.id for artist in graph_nodes}

# Add 2nd gen
nodes_counter = Counter(graph_nodes)
for artist in graph_nodes:
    nodes_counter.update(get_first_gen(artist.id))

print("Nbr nodes:", len(nodes_counter))
print("Most common:", nodes_counter.most_common(5))

graph_nodes = [artist for artist, _count in nodes_counter.most_common(500)]


node_counts = {artist.id: count for artist, count in nodes_counter.most_common(500)}

links = build_links(graph_nodes)
print("len(links):", len(links))


from scipy.cluster.hierarchy import dendrogram, linkage, leaves_list
from scipy.spatial.distance import pdist

indexed_nodes, links_by_ids = to_integer_indexed_graph(graph_nodes, links)
adjacency_matrix = np.zeros((len(indexed_nodes), len(indexed_nodes)))
for a, b in links_by_ids:
    adjacency_matrix[b, a] = 1

D = pdist(adjacency_matrix, metric="jaccard")
Z = linkage(D, method="ward", metric="jaccard", optimal_ordering=True)

labels = [indexed_nodes[node_idx].name for node_idx in leaves_list(Z)]
fig = plt.figure(figsize=(5, 12))
dn = dendrogram(Z, orientation="left", labels=labels)
plt.subplots_adjust(left=0.1, right=0.5, top=0.9, bottom=0.1)
plt.title(seed_artist.name)
plt.show()


## Sort A

cluster_sorted_nodes = {node_id: idx for idx, node_id in enumerate(leaves_list(Z))}

sorted_adjacency_matrix = np.zeros(
    (len(cluster_sorted_nodes), len(cluster_sorted_nodes))
)
for a, b in links_by_ids:
    i = cluster_sorted_nodes[a]
    j = cluster_sorted_nodes[b]
    sorted_adjacency_matrix[i, j] = 1

# print(adjacency_matrix)
fig = plt.figure(figsize=(5, 5))  # in inches
plt.imshow(sorted_adjacency_matrix, cmap="Greys", interpolation="none")
plt.show()


for node_id in leaves_list(Z):
    node = indexed_nodes[node_id]
    print(
        f"{node.name: >30} ({node.popularity: 3d}) {node.id} {node_counts[node.id]}{'*' if node.id in first_gen else ''}"
    )


#
# Export to json
#
nodes_json_data = [
    {
        "name": node.name,
        "popularity": node.popularity,
        "counts": node_counts[node.id],
        "first_gen": node.id in first_gen,
        "id": node.id,
    }
    for node in (indexed_nodes[node_id] for node_id in leaves_list(Z))
]

links_json = [
    {"source": cluster_sorted_nodes[i], "target": cluster_sorted_nodes[j], "value": 1}
    for i, j in links_by_ids
]

json_data = {"nodes": nodes_json_data, "links": links_json}
output_path = f"output/local_net_{artist_id}.json"
with open(output_path, "w") as f:
    json.dump(json_data, f)
print(f"Json saved to {output_path}")


#
# Treemap

from scipy.cluster.hierarchy import to_tree, ClusterNode

from spotigraph.treemap import iter_leaf, Rect

root = to_tree(Z)
rect = Rect(np.array([0, 1]), np.array([1, 0]))


leafs = [
    (leaf[0], indexed_nodes[leaf[1]].name)
    for leaf in iter_leaf(root, rect)
]

for c, name in leafs:
    plt.plot(*c.diag_xy(), '-o')

plt.axis('square')
plt.show()


coords = {
    leaf[1]: (leaf[0].top_left + leaf[0].bottom_right)/2
    for leaf in iter_leaf(root, rect)
}

plt.figure()


for a, b in links_by_ids:
    a_coords = coords[a]
    b_coords = coords[b]

    x = [a_coords[0], b_coords[0]]
    y = [a_coords[1], b_coords[1]]

    plt.plot(x, y, '-', alpha=0.5)
plt.axis('square')
plt.show()
