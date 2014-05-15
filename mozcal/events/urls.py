from django.conf.urls.defaults import *

from . import views

urlpatterns = patterns('',
  # Match
  url(r'^(?P<slug>[a-z0-9-]+)$', views.one, name='event.one'),
  url(r'^', views.all, name='event.all'),
)
