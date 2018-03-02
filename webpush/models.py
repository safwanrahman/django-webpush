from django.db import models
from django.core.exceptions import FieldError
from django.conf import settings

# Create your models here.


class Group(models.Model):
    name = models.CharField(max_length=255, unique=True)


class SubscriptionInfo(models.Model):
    browser = models.CharField(max_length=100)
    endpoint = models.URLField(max_length=255)
    auth = models.CharField(max_length=100)
    p256dh = models.CharField(max_length=100)


class PushInformation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='webpush_info', blank=True, null=True)
    subscription = models.ForeignKey(SubscriptionInfo, related_name='webpush_info')
    group = models.ForeignKey(Group, related_name='webpush_info', blank=True, null=True)

    def save(self, *args, **kwargs):
        # Check whether user or the group field is present
        # At least one field should be present there
        # Through from the functionality its not possible, just in case! ;)
        if self.user or self.group:
            super(PushInformation, self).save(*args, **kwargs)
        else:
            raise FieldError('At least user or group should be present')

