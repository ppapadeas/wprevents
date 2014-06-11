import random
import urllib2

from django.db import transaction
from django.db.models import Q
from django.utils import timezone
from icalendar import Calendar

from wprevents.events.models import Event, Space, FunctionalArea, EVENT_TITLE_LENGTH

default_timezone = timezone.get_default_timezone()


class Error(Exception):
  pass


def from_url(url):
  return analyze_data(fetch_url(url))


def from_file(ical_file):
  return analyze_data(ical_file.read())


def analyze_data(data):
  cal = parse_data(filter_chars(data))

  try:
    events = bulk_create_events(cal)
  except Exception, e:
    raise Error('An error occurred while bulk inserting events: ' + str(e))

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

@transaction.commit_manually
def bulk_create_events(cal):
  ical_events = [e for e in cal.walk('VEVENT')]
  duplicate_events = find_duplicates(ical_events)
  spaces = Space.objects.all()

  # Temporary bulk_id used to fetch back newly created events
  bulk_id = random.randrange(1000000000)

  # Prepare batch create by looping through ical events, filtering out duplicates
  events_to_create = []
  for e in ical_events:
    title = e.get('summary')
    # Filter out duplicate events
    if any(x.title == title for x in duplicate_events):
      continue

    start = timezone.make_naive(e.get('dtstart').dt, default_timezone)
    end = timezone.make_naive(e.get('dtend').dt, default_timezone)
    location = e.get('location')

    event = Event(
      start = start,
      end = end,
      space = guess_space(location, spaces),
      title = title[:EVENT_TITLE_LENGTH], # Truncate to avoid potential errors
      description = e.get('description').encode('utf-8'),
      bulk_id = bulk_id
    )

    # Generate slug because django's bulk_create() does not call Event.save(),
    # which is where an Event's slug is normally set
    event.define_slug()

    events_to_create.append(event)

  # Bulk create and instantly retrieve events, and remove bulk_id
  Event.objects.bulk_create(events_to_create)
  created_events = Event.objects.filter(bulk_id=bulk_id)

  # Bulk update any functional areas of all these newly created events
  FunctionalAreaRelations = Event.areas.through
  relations = []
  areas = FunctionalArea.objects.all()

  for e in created_events:
    for area in guess_functional_areas(e.description, areas):
      relations.append(FunctionalAreaRelations(event_id=e.pk, functionalarea_id=area.pk))

  FunctionalAreaRelations.objects.bulk_create(relations)

  Event.objects.filter(bulk_id=bulk_id).update(bulk_id=None);

  transaction.commit()

  return created_events


def guess_space(location, spaces):
  """
  Guess an existing Space from a string containing a raw event location
  """
  guessed_space = [s for s in spaces if s.name.lower() in location.lower()]

  return guessed_space[0] if guessed_space else None


def guess_functional_areas(description, functional_areas):
  guessed_areas = [a for a in functional_areas if a.name.lower() in description.lower()]

  return guessed_areas


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
