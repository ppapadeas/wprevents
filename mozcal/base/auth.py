from django.conf import settings
from django.contrib.auth.models import User

from django_browserid.auth import BrowserIDBackend
from django_browserid.base import get_audience

from mozcal.base.utils import get_or_create_instance


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

      return user
    else:
      return None
