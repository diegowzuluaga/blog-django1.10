from django.conf.urls import include, url

from .views import comment_hilo, comment_delete


urlpatterns = [
    url(r'^(?P<id>\d+)/$', comment_hilo, name='hilo'),
    url(r'^(?P<id>\d+)/delete/$', comment_delete, name='delete'),
]

