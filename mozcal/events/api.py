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

    serializer = MozcalSerializer(formats=['json', 'csv'])
