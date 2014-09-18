from django.utils import timezone

from tastypie import fields
from tastypie.resources import ModelResource

from wprevents.base.serializers import CustomSerializer
from models import Event, Instance, Space, FunctionalArea

def compute_resource_name(resource):
  """Compute resource name from class name, ie. 'EventResource' -> 'event'"""
  return resource.__class__.__name__[:-8].lower()


class CustomResource(ModelResource):
  def create_response(self, request, data, **response_kwargs):
    """Add HTTP header to specify the filename of CSV exports."""
    response = super(CustomResource, self).create_response(request, data, **response_kwargs)

    format = self.determine_format(request)
    extensions = {
      'text/csv': 'csv',
      'text/calendar': 'ics'
    }

    if format in extensions:
      today = timezone.now().date()
      resource_name = compute_resource_name(self)
      extension = extensions[format]
      filename = today.strftime(resource_name +'-export-%Y-%m-%d.'+ extension)
      response['Content-Disposition'] = 'filename="%s"' % filename

    return response

class EventResource(CustomResource):
  class Meta:
    queryset = Event.objects.all()
    fields = ['id', 'title', 'slug', 'start', 'end', 'city', 'country', 'description']
    filtering = {
      "title": ('startswith',),
    }

    allowed_methods = ['get']
    include_resource_uri = False
    include_absolute_url = False

    serializer = CustomSerializer(formats=['json', 'csv', 'ical'])

  def dehydrate(self, bundle):
    if bundle.obj.space:
      bundle.data['space'] = bundle.obj.space.name
    bundle.data['functional_areas'] = ','.join(bundle.obj.area_names)

    return bundle

class InstanceResource(CustomResource):
  class Meta:
    queryset = Instance.objects.all()
    fields = ['id', 'start', 'end']
    allowed_methods = ['get']
    include_resource_uri = False
    include_absolute_url = False

    serializer = CustomSerializer(formats=['csv', 'ical'])

  def dehydrate(self, bundle):
    if bundle.obj.event:
      bundle.data['event_id'] = bundle.obj.event.id
      bundle.data['title'] = bundle.obj.event.title
      bundle.data['slug'] = bundle.obj.event.slug
      bundle.data['description'] = bundle.obj.event.description
      bundle.data['functional_areas'] = ','.join(bundle.obj.event.area_names)
      if bundle.obj.event.space:
        bundle.data['space'] = bundle.obj.event.space.name

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
