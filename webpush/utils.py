# import requests
from .models import PushInformation, Group

from django.forms.models import model_to_dict

from pywebpush import WebPusher


def send_notification_to_user(user, payload, ttl=0):
    # Get all the push_info of the user
    push_infos = user.webpush_info.select_related("subscription")

    numbers = range(push_infos.count())

    for i in numbers:
        push_info = push_infos[i]
        _send_notification(push_info, payload, ttl)


def send_notification_to_group(group_name, payload, ttl=0):

    # Get all the subscription related to the group
    push_infos = Group.objects.get(name=group_name).webpush_info.select_related("subscription")
    # As there can be many subscription, iterating the large number will make it slow
    # so count the number and cut according to it
    numbers = range(push_infos.count())

    for i in numbers:
        push_info = push_infos[i]
        _send_notification(push_info, payload, ttl)


def _send_notification(push_info, payload, ttl):
    subscription = push_info.subscription
    subscription_data = _process_subscription_info(subscription)
    req = WebPusher(subscription_data).send(data=payload, ttl=ttl)
    return req

def _process_subscription_info(subscription):
    subscription_data = model_to_dict(subscription, exclude=["browser", "id"])
    endpoint = subscription_data.pop("endpoint")
    p256dh = subscription_data.pop("p256dh")
    auth = subscription_data.pop("auth")

    return {
        "endpoint": endpoint,
        "keys": {"p256dh": str(p256dh), "auth": str(auth)}
    }