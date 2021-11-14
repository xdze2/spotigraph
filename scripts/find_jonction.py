

from spotigraph.explore import get_first_gen, get_second_gen

from spotigraph.types import Artist
from spotigraph.mapeq import build_links
from spotigraph.mapeq import export_to_pajek, to_integer_graph


artist_id_a = "4ksCwAPgMi8rkQwwR3nMos"
artist_id_b = "2omAWwH1ZV9JYIyfMUQSgG"


second_gen_a = get_second_gen(artist_id_a)
second_gen_b = get_second_gen(artist_id_b)


jonction = second_gen_a & second_gen_b

for art, count in jonction.most_common():
    print(count, art.name)