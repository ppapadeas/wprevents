from django.conf.urls.defaults import url, patterns

from . import views

urlpatterns = patterns('',
  url(r'^testimport$', views.test_import, name='events_event_import'),
  url(r'^calendar$', views.calendar, name='events_event_calendar'),
  url(r'^filter_list$', views.filter_list, name='event_filter_list'),
  url(r'^filter_calendar$', views.filter_calendar, name='event_filter_calendar'),
  url(r'^spaces.json$', views.map_spaces, name='event_map_spaces'),
  url(r'^$', views.list, name='events_event_list'),
  url(r'^e/(?P<id>\w+)/(?P<start>\w+)/(?P<slug>[a-z0-9-]+)$', views.one, name='events_event_single'),
  url(r'^e/(?P<id>\w+)$', views.event_redirect_url, name='event_redirect_url'),
  url(r'^screen/(?P<slug>[a-z0-9-]+)$', views.screen, name='event_screen'),
)
