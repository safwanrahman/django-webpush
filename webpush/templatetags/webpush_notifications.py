from django import template
from django.conf import settings
from django.core.urlresolvers import reverse

register = template.Library()


@register.filter
@register.inclusion_tag('webpush.html', takes_context=True)
def webpush(context):
    group = context.get('webpush', {}).get('group')
    request = context['request']
    # If the website already provide a manifest file, we should not include it
    # into the template. If `MANIFEST` config is not provided,
    # that means we should generate a manifest by default.
    include_manifest = settings.WEBPUSH_SETTINGS.get("MANIFEST", True)
    return {'group': group, 'include_manifest': include_manifest, 'request': request}


@register.filter
@register.inclusion_tag('webpush_button.html', takes_context=True)
def webpush_button(context):
    group = context.get('webpush', {}).get('group')
    url = reverse('save_webpush_info')
    request = context['request']
    return {'group': group, 'url': url, 'request': request}
