from django.conf import settings
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType

from django_browserid.auth import BrowserIDBackend
from django_browserid.base import get_audience

from utils import get_or_create_instance
from wprevents.events.models import Event, Space, FunctionalArea


def add_permission(user, Model, codename):
  event_type = ContentType.objects.get_for_model(Model)
  permission = Permission.objects.get(content_type=event_type, codename=codename)

  user.user_permissions.add(permission)


class BrowserIDBackend(BrowserIDBackend):
  def authenticate(self, assertion=None, audience=None, request=None, **kwargs):
    if audience is None and request:
      audience = get_audience(request)

    if audience is None or assertion is None:
      return None

    verifier = self.get_verifier()
    result = verifier.verify(assertion, audience, **kwargs)

    if result.email in settings.PRIVILEGED_USERS:
      user, created = get_or_create_instance(User, username='admin')

      if created:
        user.save()

        add_permission(user, Event, 'can_administrate_events')
        add_permission(user, Space, 'can_administrate_spaces')
        add_permission(user, FunctionalArea, 'can_administrate_functional_areas')
        user.save()
      return user
    else:
      return None
