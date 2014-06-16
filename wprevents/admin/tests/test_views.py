from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase

test_username = 'admin_tester'
test_password = 'abcd1234'


class ViewsTest(TestCase):
  fixtures = ['events_test_data.json']

  def setUp(self):
    User.objects.create_superuser(username=test_username, email='test@mozilla.org', password=test_password)


  # Events
  def test_view_admin_events(self):
    """should list events in admin section"""
    self.client.login(username=test_username, password=test_password)

    response = self.client.get(reverse('event_all'))
    self.assertTemplateUsed(response, 'events.html')


  # Spaces
  def test_view_admin_spaces(self):
    """should list spaces in admin section"""
    self.client.login(username=test_username, password=test_password)

    response = self.client.get(reverse('space_all'))
    self.assertTemplateUsed(response, 'spaces.html')


  # Functional areas
  def test_view_admin_areas(self):
    """should list functional areas in admin section"""
    self.client.login(username=test_username, password=test_password)

    response = self.client.get(reverse('area_all'))
    self.assertTemplateUsed(response, 'areas.html')


