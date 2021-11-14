

from spotigraph.explore import get_first_gen, get_second_gen, get_user_library
from spotigraph.types import Artist
from spotigraph.mapeq import build_links
from spotigraph.mapeq import export_to_pajek, to_integer_graph


artist_id = "2omAWwH1ZV9JYIyfMUQSgG"



from collections import Counter

librairy_nodes = get_user_library()
nodes_counter = Counter(librairy_nodes)
for artist in librairy_nodes:
    nodes_counter.update(get_first_gen(artist.id))

print('Nbr nodes', len(nodes_counter))
print(nodes_counter.most_common(5))


graph_nodes = [artist for artist, _count in nodes_counter.most_common(500)]


links = build_links(graph_nodes)


sorted_nodes, links_by_ids = to_integer_graph(graph_nodes, links)

graph_name = 'yo'
output_path = f'output/{graph_name}.pajek'

export_to_pajek(output_path, sorted_nodes, links_by_ids)



# from infomap import Infomap

# # # Command line flags can be added as a string to Infomap
# graph = Infomap(directed=True)


# graph.add_links(links_by_ids)



# graph.run(silent=True)

# print(f"Found {graph.num_top_modules} modules with codelength: {graph.codelength}")

# print("Result")
# print("\n#node module")
# for node in graph.tree:
#     if node.is_leaf:
#         print('leaf', node.node_id, node.module_id, nodes[node.node_id].name)
#     else:
#         print(node.node_id, node.module_id)


