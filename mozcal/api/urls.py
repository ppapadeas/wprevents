from django.conf.urls.defaults import include, patterns, url

from tastypie.api import Api

from mozcal.events.api import EventResource


v1_api = Api(api_name='v1')
v1_api.register(EventResource())

urlpatterns = patterns('', url(r'', include(v1_api.urls)))