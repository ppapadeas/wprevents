from django.conf.urls.defaults import include, patterns, url

from tastypie.api import Api

from wprevents.events.api import EventResource, SpaceResource, FunctionalAreaResource


v1_api = Api(api_name='v1')
v1_api.register(EventResource())
v1_api.register(SpaceResource())
v1_api.register(FunctionalAreaResource())

urlpatterns = patterns('', url(r'', include(v1_api.urls)))