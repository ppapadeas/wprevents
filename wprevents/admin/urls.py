from django.conf.urls.defaults import include, url, patterns
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView

import views

urlpatterns = patterns('',
  url(r'^$', RedirectView.as_view(url=reverse_lazy('event_all'))),

  url(r'^events/', include([
    url(r'^$', views.events_list, name='event_all'),
    url(r'^new$', views.event_edit, name='events_new_event'),
    url(r'^delete$', views.event_delete, name='event_delete'),
    url(r'^ajax_delete$', views.event_ajax_delete, name='event_ajax_delete'),
    url(r'^import$', views.event_import_ical, name='event_import_ical'),

    url(r'^(?P<id>\w+)/', include([
      url(r'^edit', views.event_edit, name='event_edit'),
      url(r'^dedupe', views.event_dedupe, name='event_dedupe'),
    ])),
  ])),

  url(r'^spaces/', include([
    url(r'^$', views.spaces_list, name='space_all'),
    url(r'^new$', views.space_edit, name='events_new_space'),
    url(r'^delete$', views.space_delete, name='space_delete'),
    url(r'^(?P<id>\w+)/edit', views.space_edit, name='space_edit'),
  ])),

  url(r'^areas/', include([
    url(r'^$', views.area_list, name='area_all'),
    url(r'^new$', views.area_edit, name='areas_new_area'),
    url(r'^delete$', views.area_delete, name='area_delete'),
    url(r'^(?P<id>\w+)/edit', views.area_edit, name='area_edit'),
  ])),
)
