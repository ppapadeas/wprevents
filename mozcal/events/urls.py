from django.conf.urls.defaults import url, patterns

from . import views

urlpatterns = patterns('',
  url(r'^(?P<slug>[a-z0-9-]+)$', views.one, name='event_one'),
  url(r'^', views.all, name='event_all'),
)
