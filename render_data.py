from jinja2 import Template
import json

with open("template.html", "r") as f:
    template_content = f.read()
with open("data.json", "r") as f:
    data = json.load(f)

template = Template(template_content)
output = template.render(messages=data)

with open("index.html", "w") as f:
    f.write(output)
