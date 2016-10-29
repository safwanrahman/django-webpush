from django.conf import settings
from django.core.exceptions import FieldError
from django.forms.models import model_to_dict

from pywebpush import WebPusher

def send_notifications(payload, ttl, user=None, group_name=None):

    # Atleast user or group name should be provided
    if not user and not group_name:
        raise FieldError('At least user or group name should be present')

    webpush_requests = []

    if group_name:
        from .models import Group
        push_infos = Group.objects.get(name=group_name).webpush_info.select_related("subscription")

    elif user:
        push_infos = user.webpush_info.select_related("subscription")

    for push_info in push_infos:
        webpush_req = _send_notification(push_info, payload, ttl)
        webpush_requests.append(webpush_req)

    return webpush_requests

def _send_notification(push_info, payload, ttl):
    subscription = push_info.subscription
    subscription_data = _process_subscription_info(subscription)
    # Check if GCM info is provided in the settings
    if hasattr(settings,'WEBPUSH_SETTINGS'):
        gcm_key = settings.WEBPUSH_SETTINGS.get('GCM_KEY')
    else:
        gcm_key = None
    req = WebPusher(subscription_data).send(data=payload, ttl=ttl, gcm_key=gcm_key)
    return req

def _process_subscription_info(subscription):
    subscription_data = model_to_dict(subscription, exclude=["browser", "id"])
    endpoint = subscription_data.pop("endpoint")
    p256dh = subscription_data.pop("p256dh")
    auth = subscription_data.pop("auth")

    return {
        "endpoint": endpoint,
        "keys": {"p256dh": p256dh, "auth": auth}
    }
