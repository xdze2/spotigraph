


from spotigraph.explore import get_first_gen
from spotigraph.types import Artist



artist_id = "2omAWwH1ZV9JYIyfMUQSgG"

nodes = get_first_gen(artist_id)

links = []
for node in nodes:
    print('-----------')
    print(node.name)
    related_nodes = get_first_gen(node.id)
    for related in related_nodes:
        if related in nodes:
            links.append((node, related))
            print('   ', related.name)



from spotigraph.mapeq import export_to_pajek, to_integer_graph


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


