from django.conf.urls.defaults import url, patterns

from . import views

urlpatterns = patterns('',
  url(r'^events/', views.events_list, name='event_all'),
)
