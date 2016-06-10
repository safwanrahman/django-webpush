from .models import PushInformation, Group

from django.conf import settings
from django.forms.models import model_to_dict

from pywebpush import WebPusher


def send_notification_to_user(user, payload, ttl=0):
    # Get all the push_info of the user
    push_infos = user.webpush_info.select_related("subscription")
    for push_info in push_infos:
        _send_notification(push_info, payload, ttl)


def send_notification_to_group(group_name, payload, ttl=0):

    # Get all the subscription related to the group
    push_infos = Group.objects.get(name=group_name).webpush_info.select_related("subscription")
    for push_info in push_infos:
        _send_notification(push_info, payload, ttl)


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
