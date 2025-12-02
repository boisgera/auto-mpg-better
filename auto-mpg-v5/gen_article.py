from jinja2 import Template

with open("article.md.j2", mode="rt", encoding="utf-8") as template_file:
    template = Template(template_file.read())

filled = template.render(slope=14, intercept=7)

with open("article.md", mode="wt", encoding="utf-8") as article:
    article.write(filled)