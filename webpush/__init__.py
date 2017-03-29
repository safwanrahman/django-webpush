
from .utils import send_notification_to_group, send_notification_to_user


def send_group_notification(group_name, payload, ttl=0):
    send_notification_to_group(group_name, payload, ttl)


def send_user_notification(user, payload, ttl=0):
    send_notification_to_user(user, payload, ttl)
