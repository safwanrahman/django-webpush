from django import template
from django.conf import settings
from django.core.urlresolvers import reverse

register = template.Library()


@register.filter
@register.inclusion_tag('webpush.html', takes_context=True)
def webpush(context):
    group = context.get('webpush', {}).get('group')
    vapid_public_key = getattr(settings, 'WEBPUSH_SETTINGS', {}).get('VAPID_PUBLIC_KEY', '')
    request = context['request']
    return {'group': group, 'request': request, 'vapid_public_key': vapid_public_key}


@register.filter
@register.inclusion_tag('webpush_button.html', takes_context=True)
def webpush_button(context):
    group = context.get('webpush', {}).get('group')
    url = reverse('save_webpush_info')
    request = context['request']
    return {'group': group, 'url': url, 'request': request}
