import urllib2

from django.utils import timezone
from icalendar import Calendar

from wprevents.events.models import Event, Space, EVENT_TITLE_LENGTH

default_timezone = timezone.get_default_timezone()


class Error(Exception):
  pass


def from_url(url):
  return analyze_data(fetch_url(url))


def from_file(ical_file):
  return analyze_data(ical_file.read())


def analyze_data(data):
  cal = parse_data(filter_chars(data))
  events = bulk_create_events(cal)

  return events


def fetch_url(url):
  try:
    request = urllib2.Request(url)
    response = urllib2.urlopen(request)
  except urllib2.URLError:
    raise Error('Incorrect URL.')
  except ValueError:
    raise Error('Incorrect URL.')

  data = response.read().decode('utf-8')

  return data


def filter_chars(data):
  data = data.replace(u"", "") # Temp fix for Mozilla remo ics file

  return data


def parse_data(data):
  try:
    cal = Calendar.from_ical(data)
  except ValueError:
    raise Error('Error parsing icalendar file. The file may contain invalid characters.')

  return cal


def bulk_create_events(cal):
  events = []

  for ical_event in cal.walk('VEVENT'):
    start = timezone.make_naive(ical_event.get('dtstart').dt, default_timezone)
    end = timezone.make_naive(ical_event.get('dtend').dt, default_timezone)
    title = ical_event.get('summary')
    location = ical_event.get('location')

    event = Event(
      start = start,
      end = end,
      space = guess_space(location),
      title = title[:EVENT_TITLE_LENGTH], # Truncate to avoid potential errors
      description = ical_event.get('description').encode('utf-8')
    )
    # Generate slug because django's bulk_create() does not call Event.save(),
    # which is where an Event's slug is normally set
    event.define_slug()

    events.append(event)

  return Event.objects.bulk_create(events)


def guess_space(location):
  return Space.objects.get(name='Air Mozilla') or None
