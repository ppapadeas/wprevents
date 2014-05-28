from django.test import TestCase

from .models import Event

class EventTestCase(TestCase):
  def setUp(self):
    Event.objects.create(
      title="Test event",
      start="2014-05-14T14:00:00",
      end="2014-05-14T16:00:00"
    )

  def test_title_is_slugified(self):
    """event.title should be slugified on save"""
    event = Event.objects.get(title="Test event")
    self.assertEqual(event.slug, 'test-event')

