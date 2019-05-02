import json

from django.contrib import admin

from .models import PushInformation
from .utils import _send_notification

from pywebpush import WebPushException

class PushInfoAdmin(admin.ModelAdmin):
    list_display = ("__str__", "user", "subscription", "group")
    actions = ("send_test_message",)

    def send_test_message(self, request, queryset):
        payload = {"head": "Hey", "body": "Hello World"}
        for device in queryset:
            try:
                _send_notification(device.subscription, json.dumps(payload), 0)
            except WebPushException as ex:
                device.delete()
                self.message_user(request,"Deprecated subscription deleted")
        self.message_user(request,"Test sent successfully")


admin.site.register(PushInformation, PushInfoAdmin)
