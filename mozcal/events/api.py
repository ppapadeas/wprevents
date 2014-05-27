from datetime import datetime
from tastypie.resources import ModelResource
from models import Event

from mozcal.base.serializers import MozcalSerializer


class EventResource(ModelResource):
  class Meta:
    queryset = Event.objects.all()
    filtering = {
      "title": ('startswith',),
    }
    allowed_methods = ['get']
    include_resource_uri = False
    include_absolute_url = False

    serializer = MozcalSerializer(formats=['json', 'csv'])

  def create_response(self, request, data, **response_kwargs):
    """Add HTTP header to specify the filename of CSV exports."""
    response = super(EventResource, self).create_response(request, data, **response_kwargs)

    if self.determine_format(request) == 'text/csv':
      today = datetime.now().date()
      filename = today.strftime('events-export-%Y-%m-%d.csv')
      response['Content-Disposition'] = 'filename="%s"' % filename

    return response