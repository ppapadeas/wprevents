from django.conf.urls.defaults import url, patterns

from . import views

urlpatterns = patterns('',
  url(r'^calendar$', views.calendar, name='event_calendar'),
  url(r'^filter_list$', views.filter_list, name='event_filter_list'),
  url(r'^filter_calendar$', views.filter_calendar, name='event_filter_calendar'),
  url(r'^spaces.json$', views.map_spaces, name='event_map_spaces'),
  url(r'^$', views.list, name='event_list'),
  url(r'^e/(?P<id>\w+)/(?P<slug>[a-z0-9-]+)$', views.one, name='event_one'),
  url(r'^screen/(?P<slug>[a-z0-9-]+)$', views.screen, name='event_screen'),
)
