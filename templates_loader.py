from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader("templates"))
tpl = env.get_template("prompts.jinja")
