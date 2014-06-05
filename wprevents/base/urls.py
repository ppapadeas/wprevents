from django.conf.urls.defaults import url, patterns

import views

urlpatterns = patterns('',
  url(r'^login$', views.login, name='base_login'),
)
