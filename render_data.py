from jinja2 import Template
import json
from datetime import datetime, timezone
import htmlmin

with open("template.html", "r") as f:
    template_content = f.read()
with open("data.json", "r") as f:
    data = json.load(f)

template = Template(template_content)
output = template.render(messages=data, time=datetime.now(tz=timezone.utc).isoformat())
output = htmlmin.minify(output)

with open("index.html", "w") as f:
    f.write(output)
