from django.conf.urls.defaults import url, patterns

from . import views

urlpatterns = patterns('',
  url(r'^events/$', views.events_list, name='event_all'),
  url(r'^events/(?P<id>\d+)/edit', views.event_edit, name='event_edit'),
  url(r'^spaces/$', views.spaces_list, name='space_all'),
  url(r'^spaces/(?P<id>\d+)/edit', views.space_edit, name='space_edit'),
)
