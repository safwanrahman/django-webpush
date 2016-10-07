import json

from django.conf import settings
from django.core.exceptions import FieldError
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET

from .config import MANIFEST
from .forms import WebPushForm, SubscriptionForm


@require_POST
@csrf_exempt
def save_info(request):
    # Parse the  json object from post data. return 400 if the json encoding is wrong
    try:
        post_data = json.loads(request.body.decode('utf-8'))
    except ValueError:
        return HttpResponse(status=400)

    # Process the subscription data to mach with the model
    subscription_data = process_subscription_data(post_data)
    subscription_form = SubscriptionForm(subscription_data)
    # pass the data through WebPushForm for validation purpose
    web_push_form = WebPushForm(post_data)

    # Check if subscriptioninfo and the web push info bot are valid
    if subscription_form.is_valid() and web_push_form.is_valid():
        # Get the cleaned data in order to get status_type and group_name
        web_push_data = web_push_form.cleaned_data
        status_type = web_push_data.pop("status_type")
        group_name = web_push_data.pop("group")

        # We at least need the user or group to subscribe for a notification
        if request.user.is_authenticated() or group_name:
            # Save the subscription info with subscription data
            # as the subscription data is a dictionary and its valid
            subscription = subscription_form.get_or_save(subscription_data)
            web_push_form.save_or_delete(
                subscription=subscription, user=request.user,
                status_type=status_type, group_name=group_name)

            # If subscribe is made, means object is created. So return 201
            if status_type == 'subscribe':
                return HttpResponse(status=201)
            # Unsubscribe is made, means object is deleted. So return 202
            elif "unsubscribe":
                return HttpResponse(status=202)

    return HttpResponse(status=400)


@require_GET
def generate_manifest(request):
    if hasattr(settings,'WEBPUSH_SETTINGS'):
        return JsonResponse(MANIFEST)
    else:
        return HttpResponse(status=404)


def process_subscription_data(post_data):
    """Process the subscription data according to out model"""
    subscription_data = post_data.pop("subscription", {})
    # As our database saves the auth and p256dh key in separate field,
    # we need to refactor it and insert the auth and p256dh keys in the same dictionary
    keys = subscription_data.pop("keys", {})
    subscription_data.update(keys)
    # Insert the browser name
    subscription_data["browser"] = post_data.pop("browser")
    return subscription_data
