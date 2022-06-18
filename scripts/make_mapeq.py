from collections import Counter
from infomap import Infomap

import matplotlib.pyplot as plt
import numpy as np

from spotigraph.explore import get_first_gen, get_second_gen, get_user_library
from spotigraph.network import build_links, export_to_pajek, to_integer_graph
from spotigraph.types import Artist


# artist_id = "2omAWwH1ZV9JYIyfMUQSgG"
artist_id ='0GtJweTzG1ECJ78loPQxzl'

librairy_nodes = get_first_gen(artist_id)  # get_user_library()

nodes_counter = Counter(librairy_nodes)
for artist in librairy_nodes:
    nodes_counter.update(get_first_gen(artist.id))

print("Nbr nodes:", len(nodes_counter))
print("Most common:", nodes_counter.most_common(5))


graph_nodes = [artist for artist, _count in nodes_counter.most_common(500)]

links = build_links(graph_nodes)

print("len(links):", len(links))

# ---------------
# Export to pajek
# ---------------
# sorted_nodes, links_by_ids = to_integer_graph(graph_nodes, links)

# graph_name = "yo"
# output_path = f"output/{graph_name}.pajek"

# export_to_pajek(output_path, sorted_nodes, links_by_ids)


# -------
# InfoMap
# -------


# # # Command line flags can be added as a string to Infomap
graph = Infomap(directed=True)

sorted_nodes, links_by_ids = to_integer_graph(graph_nodes, links)
graph.add_links(links_by_ids)


graph.run(silent=True)

print(f"Found {graph.num_top_modules} modules with codelength: {graph.codelength}")


for key, mod in graph.get_modules(depth_level=1).items():
    print(key, mod)


# -----
# Adj.
# ----


from scipy.cluster.hierarchy import dendrogram, linkage, leaves_list
from scipy.spatial.distance import pdist


adjacency_matrix = np.zeros((len(sorted_nodes), len(sorted_nodes)))
for a, b in links_by_ids:
    adjacency_matrix[a, b] = 1

D = pdist(adjacency_matrix, metric="jaccard")
Z = linkage(D, method="ward", metric="jaccard", optimal_ordering=True)

print(Z)

fig = plt.figure(figsize=(25, 10))
dn = dendrogram(Z)
plt.show()

## Sort A

cluster_sorted_nodes = {node_id: idx for idx, node_id in enumerate(leaves_list(Z))}

sorted_adjacency_matrix = np.zeros((len(cluster_sorted_nodes), len(cluster_sorted_nodes)))
for a, b in links_by_ids:
    i = cluster_sorted_nodes[a]
    j = cluster_sorted_nodes[b]
    adjacency_matrix[i, j] = 1

# print(adjacency_matrix)
fig = plt.figure(figsize=(5, 5))  # in inches
plt.imshow(adjacency_matrix, cmap="Greys", interpolation="none")
plt.show()


for node_id in leaves_list(Z):
    node = sorted_nodes[node_id]
    print(f"{node.name: >30} ({node.popularity: 3d})")

    # links_to = [link for link in links if link[0] == node_id]
    # print(links_to)
# The rest is just if you have sorted nodes by a partition and want to
# highlight the module boundaries
# assert len(partitions) == len(colors)
# ax = pyplot.gca()
# for partition, color in zip(partitions, colors):
#     current_idx = 0
#     for module in partition:
#         ax.add_patch(
#             patches.Rectangle(
#                 (current_idx, current_idx),
#                 len(module),  # Width
#                 len(module),  # Height
#                 facecolor="none",
#                 edgecolor=color,
#                 linewidth="1",
#             )
#         )
#         current_idx += len(module)

# print("Result")
# print("\n#node module")
# for node in graph.tree:
#     if node.is_leaf:
#         print('leaf', node.node_id, node.module_id, nodes[node.node_id].name)
#     else:
#         print(node.node_id, node.module_id)
