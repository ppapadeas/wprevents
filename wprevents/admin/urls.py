from django.conf.urls.defaults import include, url, patterns
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView

import views

urlpatterns = patterns('',
  url(r'^$', RedirectView.as_view(url=reverse_lazy('admin_event_list'))),

  url(r'^events/', include([
    url(r'^$', views.events_list, name='admin_event_list'),
    url(r'^new$', views.event_edit, name='admin_event_new'),
    url(r'^delete$', views.event_delete, name='admin_event_delete'),
    url(r'^ajax_delete$', views.event_ajax_delete, name='admin_event_ajax_delete'),
    url(r'^import$', views.event_import_ical, name='admin_event_import_ical'),

    url(r'^(?P<id>\w+)/', include([
      url(r'^edit', views.event_edit, name='admin_event_edit'),
      url(r'^dedupe', views.event_dedupe, name='admin_event_dedupe'),
    ])),
  ])),

  url(r'^spaces/', include([
    url(r'^$', views.spaces_list, name='admin_spaces_all'),
    url(r'^new$', views.space_edit, name='admin_space_new'),
    url(r'^delete$', views.space_delete, name='admin_space_delete'),
    url(r'^(?P<id>\w+)/edit', views.space_edit, name='admin_space_edit'),
  ])),

  url(r'^areas/', include([
    url(r'^$', views.area_list, name='admin_area_list'),
    url(r'^new$', views.area_edit, name='admin_area_new'),
    url(r'^delete$', views.area_delete, name='admin_area_delete'),
    url(r'^(?P<id>\w+)/edit', views.area_edit, name='admin_area_edit'),
  ])),
)
