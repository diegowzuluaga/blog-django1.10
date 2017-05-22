from django.conf.urls import include, url

from . import views
'''
asi tambien vale hacer las importaciones:
from .views import (
	post_list,
	post_create,
	etc,
	)
'''

urlpatterns = [
    url(r'^$', views.post_list, name='list'),
    url(r'^create/$', views.post_create, name='create'),
    url(r'^(?P<slug>[\w-]+)/$', views.post_detail, name='detail'),
    url(r'^(?P<slug>[\w-]+)/edit/$', views.post_update, name='update'),
    url(r'^(?P<slug>[\w-]+)/delete/$', views.post_delete, name='delete'),
]
