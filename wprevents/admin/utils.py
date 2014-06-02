import urllib2

from django.utils import timezone
from icalendar import Calendar

from wprevents.events.models import Event, Space, EVENT_TITLE_LENGTH

default_timezone = timezone.get_default_timezone()


class ImportIcalError(Exception):
  pass


def import_ical(url):
  try:
    request = urllib2.Request(url)
    response = urllib2.urlopen(request)
  except urllib2.URLError:
    raise ImportIcalError('Incorrect URL.')
  except ValueError:
    raise ImportIcalError('Incorrect URL.')

  data = response.read().decode('utf-8')
  data = data.replace(u"", "") # Temp fix for Mozilla remo ics file

  try:
    cal = Calendar.from_ical(data)
  except ValueError:
    raise ImportIcalError('Error parsing icalendar file. The file may contain invalid characters.')

  return bulk_create_events(cal)


def bulk_create_events(cal):
  air_mozilla_space = Space.objects.get(name='Air Mozilla')
  events = []

  for ical_event in cal.walk('VEVENT'):
    start = timezone.make_naive(ical_event.get('dtstart').dt, default_timezone)
    end = timezone.make_naive(ical_event.get('dtend').dt, default_timezone)
    title = ical_event.get('summary')

    event = Event(
      start = start,
      end = end,
      space = air_mozilla_space,
      title = title[:EVENT_TITLE_LENGTH], # Truncate to avoid potential errors
      description = ical_event.get('description').encode('utf-8')
    )
    # Generate slug because django's bulk_create() does not call Event.save(),
    # which is where an Event's slug is normally set
    event.define_slug()

    events.append(event)

  return Event.objects.bulk_create(events)
