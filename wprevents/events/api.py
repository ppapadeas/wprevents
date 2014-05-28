from datetime import datetime

from tastypie import fields
from tastypie.resources import ModelResource

from wprevents.base.serializers import CustomSerializer
from models import Event, Space, FunctionalArea


class CustomResource(ModelResource):
  def create_response(self, request, data, **response_kwargs):
    """Add HTTP header to specify the filename of CSV exports."""
    response = super(CustomResource, self).create_response(request, data, **response_kwargs)

    if self.determine_format(request) == 'text/csv':
      today = datetime.now().date()

      # Compute resource name from class name, ie. 'EventResource' -> 'event'
      resource_name = self.__class__.__name__[:-8].lower()
      filename = today.strftime(resource_name +'-export-%Y-%m-%d.csv')
      response['Content-Disposition'] = 'filename="%s"' % filename

    return response

class EventResource(CustomResource):
  class Meta:
    queryset = Event.objects.all()
    fields = ['title', 'start', 'end']
    filtering = {
      "title": ('startswith',),
    }

    allowed_methods = ['get']
    include_resource_uri = False
    include_absolute_url = False

    serializer = CustomSerializer(formats=['json', 'csv'])

  def dehydrate(self, bundle):
    bundle.data['space'] = bundle.obj.space.name
    bundle.data['functional_areas'] = ','.join(bundle.obj.area_names)
    return bundle


class SpaceResource(CustomResource):
  class Meta:
    queryset = Space.objects.all()
    fields = ['name', 'address', 'address2', 'city', 'country', 'lat', 'lon', 'photo_url']

    allowed_methods = ['get']
    include_resource_uri = False
    include_absolute_url = False

    serializer = CustomSerializer(formats=['csv'])


class FunctionalAreaResource(CustomResource):
  class Meta:
    queryset = FunctionalArea.objects.all()
    fields = ['name', 'slug', 'color']

    allowed_methods = ['get']
    include_resource_uri = False
    include_absolute_url = False

    serializer = CustomSerializer(formats=['csv'])
