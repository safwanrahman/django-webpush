from django import template
from django.conf import settings
from django.urls import reverse

from webpush.utils import get_templatetag_context

register = template.Library()


@register.filter
@register.inclusion_tag('webpush_header.html', takes_context=True)
def webpush_header(context):
    template_context = get_templatetag_context(context)
    return template_context


@register.filter
@register.inclusion_tag('webpush_button.html', takes_context=True)
def webpush_button(context):
    template_context = get_templatetag_context(context)
    return template_context
