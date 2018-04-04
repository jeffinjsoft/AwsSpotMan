from django.conf.urls import url,include
from django.contrib import admin
from . import views



urlpatterns = [
    url(r'^$', views.index),
    url(r'stacks/$', views.stacks),
    url(r'stacks/view/(?P<s_id>[0-9]+)/$', views.stack_view),
    url(r'stacks/view_del/(?P<s_id>[0-9]+)/$', views.stack_view_del),
    url(r'stacks/refresh/(?P<s_id>[0-9]+)/$', views.refresh_status),
    url(r'stacks/add/$', views.stacks_add),
    url(r'stacks/start/(?P<s_id>[0-9]+)/$', views.stack_start),
]
