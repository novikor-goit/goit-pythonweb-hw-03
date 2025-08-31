from jinja2 import Environment, FileSystemLoader


class Renderer:
    def __init__(self, template_dir="./templates"):
        self.env = Environment(loader=FileSystemLoader(template_dir))

    def render(self, template_name, data):
        template = self.env.get_template(template_name)
        return template.render(data)
