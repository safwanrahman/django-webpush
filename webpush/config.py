from django.conf import settings

MANIFEST = {}
if hasattr(settings,'WEBPUSH_SETTINGS'):
    MANIFEST["gcm_sender_id"] = settings.WEBPUSH_SETTINGS['GCM_ID']
