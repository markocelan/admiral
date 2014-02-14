from django.conf.urls import patterns, url
from django.conf import settings
from supervisors import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        url(r'^inst/(?P<server_id>\d+)/$', views.inst, name='inst'),
        url(r'^inst/(?P<server_id>\d+)/action/(?P<action_name>\w+)/(?P<process_name>[\w\.\:\-]+)/$', views.action,  name='action'),
#        url(r'^(?P<app_key>\w+)/ping/$', views.ping, name='ping'),
#        url(r'^(?P<app_key>\w+)/status/$', views.status, name='status'),
)
if settings.DEBUG:
    urlpatterns += patterns('django.contrib.staticfiles.views',
        url(r'^static/(?P<path>.*)$', 'serve'),
    )
