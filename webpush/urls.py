from django.urls import path
from django.views.i18n import JavaScriptCatalog

from django.views.decorators.cache import cache_page
from django.utils import timezone
from . import views

# When we last restarted the server; used for cache control headers and
# invalidating the server side cache on server restart
last_modified_date = timezone.now().strftime("%Y-%m-%d_%H:%M:%S")

urlpatterns = [
    path('jsi18n/',
         cache_page(86400, key_prefix='js18n-%s' % last_modified_date)(
             JavaScriptCatalog.as_view(packages=['webpush'])
         ),
         name='javascript-catalog'),
    path('save_information', views.save_info, name='save_webpush_info'),
    # Service worker need to be loaded from same domain
    path('service-worker.js', views.ServiceWorkerView.as_view(), name='service_worker')
]
