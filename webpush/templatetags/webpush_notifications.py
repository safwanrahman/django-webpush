from django import template
from django.core.urlresolvers import reverse

register = template.Library()


@register.filter
@register.inclusion_tag('webpush.html', takes_context=True)
def webpush(context):
    group = context.get('webpush', {}).get('group')
    request = context['request']
    return {'group': group, 'request': request}


@register.filter
@register.inclusion_tag('manifest.html', takes_context=True)
def webpush_manifest(context):
    group = context.get('webpush', {}).get('group')
    request = context['request']
    return {'group': group, 'request': request}


@register.filter
@register.inclusion_tag('webpush_button.html', takes_context=True)
def webpush_button(context):
    group = context.get('webpush', {}).get('group')
    url = reverse('save_webpush_info')
    request = context['request']
    return {'group': group, 'url': url, 'request': request}
