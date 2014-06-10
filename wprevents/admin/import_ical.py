import urllib2

from django.db.models import Q
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
  except urllib2.URLError, e:
    raise Error('URL: error' + str(e.reason))
  except urllib2.HTTPError, e:
    raise Error('HTTP error: ' + str(e.code))

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

  ical_events = [e for e in cal.walk('VEVENT')]
  duplicate_events = find_duplicates(ical_events)

  all_spaces = Space.objects.all()

  # Prepare bulk insertion, filter out items previously seen as duplicates
  for e in ical_events:
    title = e.get('summary')

    if any(x.title == title for x in duplicate_events):
      # Skip the events if already added
      continue

    start = timezone.make_naive(e.get('dtstart').dt, default_timezone)
    end = timezone.make_naive(e.get('dtend').dt, default_timezone)
    location = e.get('location')

    event = Event(
      start = start,
      end = end,
      space = guess_space(location, all_spaces),
      title = title[:EVENT_TITLE_LENGTH], # Truncate to avoid potential errors
      description = e.get('description').encode('utf-8')
    )
    # Generate slug because django's bulk_create() does not call Event.save(),
    # which is where an Event's slug is normally set
    event.define_slug()

    events.append(event)

  return Event.objects.bulk_create(events)


def guess_space(location, spaces):
  """
  Guess an existing Space from a string containing a raw event location
  """
  guessed_space = [s for s in spaces if s.name.lower() in location.lower()]

  return guessed_space[0] if guessed_space else None


def find_duplicates(ical_events):
  """
  Return all events previously added in the database that would be duplicate candidates (ie. same title, same start date) of all events provided in the
    imported ical file.
  """
  titles = []
  start_dates = []

  for e in ical_events:
    titles.append(e.get('summary'))
    start_dates.append(timezone.make_naive(e.get('dtstart').dt, default_timezone))

  # Dynamically build 'or' filters
  filter_titles = reduce(lambda q, e: q|Q(title=e.title), titles, Q())
  filter_start_dates = reduce(lambda q, date: q|Q(start=date), start_dates, Q())

  return Event.objects.filter(filter_titles|filter_start_dates)
