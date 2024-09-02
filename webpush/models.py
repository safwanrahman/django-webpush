from django.db import models
from django.core.exceptions import FieldError
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class Group(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name=_("Name"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Group")
        verbose_name_plural = _("Groups")
        ordering = ['name']


class SubscriptionInfo(models.Model):
    browser = models.CharField(max_length=100, verbose_name=_("Browser"))
    user_agent = models.CharField(max_length=500, blank=True, verbose_name=_("User Agent"))
    endpoint = models.URLField(max_length=500, verbose_name=_("Endpoint"))
    auth = models.CharField(max_length=100, verbose_name=_("Auth"))
    p256dh = models.CharField(max_length=100, verbose_name=_("P256DH"))

    def __str__(self):
        return self.browser

    class Meta:
        verbose_name = _("Subscription Info")
        verbose_name_plural = _("Subscription Infos")
        ordering = ['browser']


class PushInformation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='webpush_info', blank=True, null=True, on_delete=models.CASCADE, verbose_name=_("User"))
    subscription = models.ForeignKey(SubscriptionInfo, related_name='webpush_info', on_delete=models.CASCADE, verbose_name=_("Subscription"))
    group = models.ForeignKey(Group, related_name='webpush_info', blank=True, null=True, on_delete=models.CASCADE, verbose_name=_("Group"))

    def save(self, *args, **kwargs):
        # Check whether user or the group field is present
        # At least one field should be present there
        # Through from the functionality its not possible, just in case! ;)
        if self.user or self.group:
            super(PushInformation, self).save(*args, **kwargs)
        else:
            raise FieldError(_('At least user or group should be present'))

    def __str__(self):
        if self.group:
            return self.group

        return self.user

    class Meta:
        verbose_name = _("Push Information")
        verbose_name_plural = _("Push Information")
        ordering = ['user', 'group']
