

from spotigraph.explore import get_first_gen, get_second_gen
from spotigraph.types import Artist
from spotigraph.mapeq import build_links
from spotigraph.mapeq import export_to_pajek, to_integer_graph


artist_id = "2omAWwH1ZV9JYIyfMUQSgG"


second_gen = get_second_gen(artist_id)


nodes = [artist for artist, _count in second_gen.most_common(20)]


links = build_links(nodes)


sorted_nodes, links_by_ids = to_integer_graph(nodes, links)

graph_name = 'yo'
output_path = f'output/{graph_name}.pajek'

export_to_pajek(output_path, sorted_nodes, links_by_ids)




from infomap import Infomap

# # Command line flags can be added as a string to Infomap
graph = Infomap(directed=True)


graph.add_links(links_by_ids)



graph.run(silent=True)

print(f"Found {graph.num_top_modules} modules with codelength: {graph.codelength}")

print("Result")
print("\n#node module")
for node in graph.tree:
    if node.is_leaf:
        print('leaf', node.node_id, node.module_id, nodes[node.node_id].name)
    else:
        print(node.node_id, node.module_id)


