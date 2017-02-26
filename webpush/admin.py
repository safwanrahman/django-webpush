from django.contrib import admin

from .models import PushInformation
from .utils import _send_notification


class PushInfoAdmin(admin.ModelAdmin):
    list_display = ("__str__", "user", "subscription", "group")
    actions = ("send_message",)

    def send_message(self, request, queryset):
        result = []
        payload = "{\"head\": \"Hey\", \"body\": \"Hello World\"}"
        for device in queryset:
            result.append(_send_notification(device, payload, '0'))

admin.site.register(PushInformation, PushInfoAdmin)
