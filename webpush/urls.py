from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^save_information', views.save_info, name='save_webpush_info'),
    url(r'^manifest', views.generate_manifest, name='webpush_manifest_json'),
]
