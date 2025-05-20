# templates_loader.py
from jinja2 import Environment, FileSystemLoader, select_autoescape

env = Environment(
    loader=FileSystemLoader("templates"),
    autoescape=select_autoescape()
)

# Carga el fichero prompts.jinja
tpl = env.get_template("prompts.jinja")

