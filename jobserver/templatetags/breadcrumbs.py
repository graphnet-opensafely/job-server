from django import template


register = template.Library()


@register.inclusion_tag("breadcrumb-item.html", name="breadcrumb-item")
def breadcrumb_item(path, text):
    return {
        "path": path,
        "text": text,
    }


@register.inclusion_tag("breadcrumb-current.html", name="breadcrumb-current")
def breadcrumb_current(text):
    return {"text": text}


@register.tag()
def breadcrumb(parser, token):
    nodes = parser.parse(("endbreadcrumb",))
    parser.delete_first_token()
    return CommentNode(nodes)


class CommentNode(template.Node):
    def __init__(self, nodes):
        super().__init__()
        self._nodes = nodes

    def render(self, context):
        items = [node.render(context) for node in self._nodes]
        new_context = context.new({"items": items})
        t = context.template.engine.get_template("breadcrumb.html")
        return t.render(new_context)
