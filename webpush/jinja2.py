import arrow
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from jinja2 import contextfunction

from jinja2 import nodes
from jinja2.ext import Extension
from markupsafe import Markup

from webpush.utils import get_templatetag_context


class WebPushExtension(Extension):

    def __init__(self, environment):
        super(WebPushExtension, self).__init__(environment)
        environment.globals['webpush_header'] = self.webpush_header
        environment.globals['webpush_button'] = self.webpush_button

    @contextfunction
    def webpush_header(self, context):
        template_context = get_templatetag_context(context)
        data = render_to_string('webpush_header.html', template_context, using='django')
        return mark_safe(data)

    @contextfunction
    def webpush_button(self, context, with_class=None):
        template_context = get_templatetag_context(context)
        if with_class:
            template_context['class'] = with_class
        data = render_to_string('webpush_button.html', template_context, using='django')
        return mark_safe(data)
