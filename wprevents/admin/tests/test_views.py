from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase

from wprevents.events.models import Event

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
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'events.html')

    # Delete and dedupe
  def test_view_admin_events_delete_logged_in(self):
    """should delete/dedupe an event when logged in"""
    self.client.login(username=test_username, password=test_password)
    response = self.client.post(reverse('event_ajax_delete'), { 'id': 1 }, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

    self.assertEqual(response.status_code, 200)
    self.assertEqual(Event.objects.filter(pk=1).exists(), False)


  def test_view_admin_events_delete_not_logged_out(self):
    """should delete/dedupe an event when not logged in"""
    response = self.client.post(reverse('event_ajax_delete'), { 'id': 1 }, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

    self.assertEqual(response.status_code, 302)
    self.assertEqual(Event.objects.filter(pk=1).exists(), True)


  # Spaces
  def test_view_admin_spaces(self):
    """should list spaces in admin section"""
    self.client.login(username=test_username, password=test_password)

    response = self.client.get(reverse('space_all'))
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'spaces.html')


  # Functional areas
  def test_view_admin_areas(self):
    """should list functional areas in admin section"""
    self.client.login(username=test_username, password=test_password)

    response = self.client.get(reverse('area_all'))
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'areas.html')
