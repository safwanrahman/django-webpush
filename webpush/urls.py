from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^save_information', views.save_info, name='save_webpush_info'),
    # Service worker need to be loaded from same domain
    url(r'^service-worker.js', views.ServiceWorkerView.as_view(), name='service_worker')
]
