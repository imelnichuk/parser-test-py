from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<region_id>[0-9]+)/$', views.region_data, name='region_data'),
]
