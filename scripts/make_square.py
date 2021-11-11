
from pathlib import Path
from jinja2 import Template

from spotigraph.explore import get_second_gen


artist_id = "0wf6vuNqTvdRGrmpsPu2kW"

second_gen = get_second_gen(artist_id)

print(second_gen)
print(len(second_gen))

top_one = second_gen.most_common(5)[0][0]
print(top_one)


template_src = """
<html>
<style>
body {
    background-color: black;
}
img {
    margin: 0;
    padding: 0;
    border: 0;
}
</style>
<body>

{% for arti in artists -%}
    <img src="{{arti.image}}">
{% endfor %}

</body>
</html>
"""


j2_template = Template(template_src)

Path('output').mkdir(parents=True, exist_ok=True)
data = [elt.asdict() for elt, count in second_gen.most_common()]
with open('output/square.html', 'w') as f:
    f.write(j2_template.render({'artists': data}))

print('HTMl saved')