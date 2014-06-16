from django.test import TestCase

from django.core.urlresolvers import reverse

class ViewsTest(TestCase):
  def test_view_events_as_list(self):
    """should view events as list"""
    response = self.client.get(reverse('event_list'))
    self.assertTemplateUsed(response, 'list.html')


  def test_view_events_as_calendar(self):
    """should view events as calendar"""
    response = self.client.get(reverse('event_calendar'))
    self.assertTemplateUsed(response, 'calendar.html')
