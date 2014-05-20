from django.conf.urls.defaults import url, patterns

from . import views

urlpatterns = patterns('',
  url(r'^events/$', views.events_list, name='event_all'),
  url(r'^events/(?P<slug>[a-z0-9-]+)/edit', views.event_edit, name='event_edit'),
  url(r'^events/new$', views.event_edit, name='events_new_event'),
  url(r'^events/delete$', views.event_delete, name='event_delete'),
  url(r'^events/(?P<slug>[a-z0-9-]+)/dedupe', views.event_dedupe, name='event_dedupe'),

  url(r'^spaces/$', views.spaces_list, name='space_all'),
  url(r'^spaces/(?P<slug>[a-z0-9-]+)/edit', views.space_edit, name='space_edit'),
  url(r'^spaces/new$', views.space_edit, name='events_new_space'),
  url(r'^spaces/delete$', views.space_delete, name='space_delete'),
)
