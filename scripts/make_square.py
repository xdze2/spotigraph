
from pathlib import Path
from jinja2 import Template

from spotigraph.explore import get_second_gen, get_first_gen


artist_id = "0wf6vuNqTvdRGrmpsPu2kW"

first_gen = get_first_gen(artist_id)
second_gen = get_second_gen(artist_id)


print('2nd gen:', len(second_gen))

for arti, count in second_gen.most_common(30):
    is_in_first = arti in first_gen
    is_in_first_label = "x" if is_in_first else ' '
    print(f'{count:3d}', is_in_first_label, arti.name)


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
    border-radius: 50%;
}

.tooltip {
  position: relative;
  display: inline-block;
}

/* Tooltip text */
.tooltip .tooltiptext {
  visibility: hidden;
  width: 120px;
  background-color: gray;
  color: #fff;
  text-align: center;
  padding: 5px 0;
  border-radius: 6px;
 
  /* Position the tooltip text - see examples below! */
  position: absolute;
  z-index: 1;
}

/* Show the tooltip text when you mouse over the tooltip container */
.tooltip:hover .tooltiptext {
  visibility: visible;
}
</style>
<body>

{% for arti in artists -%}
    <div class="tooltip">
        <img src="{{arti.image}}" width="{{arti.size}}px" height="{{arti.size}}px">
        <span class="tooltiptext">{{arti.name}}</span>
    </div> 
{% endfor %}

</body>
</html>
"""


j2_template = Template(template_src)

Path('output').mkdir(parents=True, exist_ok=True)
data = [
    {
        **elt.asdict(),
        'size':18 + 10*count
    }
    for elt, count in second_gen.most_common(30)
]
with open('output/square.html', 'w') as f:
    f.write(j2_template.render({'artists': data}))

print('HTMl saved')