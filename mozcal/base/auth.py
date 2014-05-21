from django.conf import settings

from django_browserid.auth import BrowserIDBackend


class CustomBackend(BrowserIDBackend):
  def filter_users_by_email(self, email):
    # Check for existence of email address in a list of two-tuples
    is_admin = [i for i, v in enumerate(settings.PRIVILEGED_USERS) if v[0] == email]

    return is_admin
