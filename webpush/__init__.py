import json

from .utils import send_notifications


def send_group_notification(group_name, payload, ttl=0):
    payload = json.dumps(payload)
    webpush_requests = send_notifications(group_name, payload, ttl)
    return webpush_requests


def send_user_notification(user, payload, ttl=0):
    payload = json.dumps(payload)
    webpush_requests = send_notifications(user, payload, ttl)
    return webpush_requests
