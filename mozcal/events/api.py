from datetime import datetime
from tastypie.resources import ModelResource
from models import Event, Space, FunctionalArea

from mozcal.base.serializers import MozcalSerializer


class MozcalResource(ModelResource):
  def create_response(self, request, data, **response_kwargs):
    """Add HTTP header to specify the filename of CSV exports."""
    response = super(MozcalResource, self).create_response(request, data, **response_kwargs)

    if self.determine_format(request) == 'text/csv':
      today = datetime.now().date()

      # Compute resource name from class name, ie. 'EventResource' -> 'event'
      resource_name = self.__class__.__name__[:-8].lower()
      filename = today.strftime(resource_name +'-export-%Y-%m-%d.csv')
      response['Content-Disposition'] = 'filename="%s"' % filename

    return response


class EventResource(MozcalResource):
  class Meta:
    queryset = Event.objects.all()
    fields = ['title', 'space', 'start', 'end', 'area_names']
    filtering = {
      "title": ('startswith',),
    }

    allowed_methods = ['get']
    include_resource_uri = False
    include_absolute_url = False

    serializer = MozcalSerializer(formats=['json', 'csv'])


class SpaceResource(MozcalResource):
  class Meta:
    queryset = Space.objects.all()
    fields = ['name', 'address', 'address2', 'city', 'country', 'lat', 'lon', 'photo_url']

    allowed_methods = ['get']
    include_resource_uri = False
    include_absolute_url = False

    serializer = MozcalSerializer(formats=['csv'])


class FunctionalAreaResource(MozcalResource):
  class Meta:
    queryset = FunctionalArea.objects.all()
    fields = ['name', 'slug', 'color']

    allowed_methods = ['get']
    include_resource_uri = False
    include_absolute_url = False

    serializer = MozcalSerializer(formats=['csv'])
