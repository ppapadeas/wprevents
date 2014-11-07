from datetime import datetime, date, time
from HTMLParser import HTMLParser
import random
import urllib2

from django.conf import settings
from django.db import transaction
from django.db.models import Q
from django.utils import timezone
from icalendar import Calendar
import pytz

from wprevents.events.models import Event, Space, FunctionalArea, EVENT_TITLE_LENGTH
from wprevents.base.tasks import generate_event_instances

from recurrence import *
from dateutil.rrule import rruleset, rrulestr


class EventImporterError(Exception):
  pass

class EventImporter:
  def __init__(self, space=None):
    self.space = space
    self.spaces = Space.objects.all()

  def from_url(self, url):
    return self.from_string(self.fetch_url(url))

  def from_string(self, data):
    cal = self.parse_data(self.sanitize(data))

    try:
      events, skipped = self.bulk_create_events(cal)
      generate_event_instances.delay()
    except transaction.TransactionManagementError, e:
      transaction.rollback()
      raise EventImporterError('An error with the database transaction occured while bulk inserting events: ' + str(e))
    except Exception, e:
      raise EventImporterError('An error occurred while bulk inserting events: ' + str(e))

    return events, skipped


  def fetch_url(self, url):
    try:
      request = urllib2.Request(url)
      response = urllib2.urlopen(request)
    except urllib2.URLError, e:
      raise EventImporterError('URL: error' + str(e.reason))
    except urllib2.HTTPError, e:
      raise EventImporterError('HTTP error: ' + str(e.code))

    data = response.read().decode('utf-8')

    return data


  def sanitize(self, data):
    data = data.replace(u"", "") # Temp fix for Mozilla remo ICS file

    return data


  def parse_data(self, data):
    try:
      cal = Calendar.from_ical(data)
    except ValueError:
      raise EventImporterError('Error parsing icalendar file. The file may contain invalid characters.')

    return cal

  @transaction.commit_manually
  def bulk_create_events(self, cal):
    ical_events = [e for e in cal.walk('VEVENT')]
    duplicate_candidates = self.find_duplicate_candidates(ical_events)

    # Temporary bulk_id used to fetch back newly created events
    bulk_id = random.randrange(1000000000)

    # Prepare batch create by looping through ical events, filtering out duplicates
    events_to_create = []
    recurrences = []
    skipped = 0
    for ical_event in ical_events:
      title = HTMLParser().unescape(ical_event.get('summary'))
      title = title[:EVENT_TITLE_LENGTH] # Truncate to avoid potential errors

      location = ical_event.get('location', '')
      description = ical_event.get('description', '')
      description = HTMLParser().unescape(description).encode('utf-8')

      if self.space is None:
        # Auto-detection is disabled for now
        # (Space field in import modal is required=True)
        space = self.guess_space(location)
      else:
        space = self.space

      start = self.convert_datetime(ical_event.get('dtstart').dt, space)
      end = self.convert_datetime(ical_event.get('dtend').dt, space)

      # We always want to store datetimes as UTC
      start = timezone.make_naive(start, pytz.utc)
      end = timezone.make_naive(end, pytz.utc)

      # Filter out duplicate events
      if any(self.is_duplicate(e, start, title, space) for e in duplicate_candidates):
        skipped += 1
        continue

      event = Event(
        start = start,
        end = end,
        space = space,
        title = title,
        description = description,
        bulk_id = bulk_id
      )

      # Generate slug because django's bulk_create() does not call Event.save(),
      # which is where an Event's slug is normally set
      event.define_slug()

      # Also update start and end datetimes in local time (relative to space)
      event.update_local_datetimes()

      events_to_create.append(event)

      recurrences.append(self.get_recurrence(ical_event, event))

    # Bulk create and instantly retrieve events, and remove bulk_id
    Event.objects.bulk_create(events_to_create)
    created_events = Event.objects.filter(bulk_id=bulk_id)

    # Bulk update any functional areas of all these newly created events
    FunctionalAreaRelations = Event.areas.through
    relations = []
    areas = FunctionalArea.objects.all()

    for i, event in enumerate(created_events):
      if recurrences[i] is not None:
        event.recurrence = recurrences[i]
        event.save()

      for area in self.guess_functional_areas(event.description, areas):
        relations.append(FunctionalAreaRelations(event_id=event.pk, functionalarea_id=area.pk))

    FunctionalAreaRelations.objects.bulk_create(relations)

    Event.objects.filter(bulk_id=bulk_id).update(bulk_id=None);

    transaction.commit()

    return created_events, skipped


  def guess_space(self, location):
    """
    Guess an existing Space from a string containing a raw event location
    """
    guessed_space = [s for s in self.spaces if s.name.lower() in location.lower()]

    return guessed_space[0] if guessed_space else None


  def guess_functional_areas(self, description, functional_areas):
    guessed_areas = [a for a in functional_areas if a.name.lower() in description.lower()]

    return guessed_areas

  def convert_datetime(self, dt, space):
    if isinstance(dt, date) and not isinstance(dt, datetime):
      # If there is no time specified for this dt,
      # convert it to a datetime object with a time set to 00:00
      dt = datetime.combine(dt, time(0, 0, 0))

      if space and space.timezone:
        # If the event space is known, make it local to its timezone
        dt = pytz.timezone(space.timezone).localize(dt)
      else:
        dt = pytz.utc.localize(dt)

    return dt

  def find_duplicate_candidates(self, ical_events):
    """
    Return all events previously added in the database that would be duplicate candidates (ie. same title, same start date) of all events provided in the
      imported ical file.
    """
    titles = []
    start_dates = []

    for ical_event in ical_events:
      titles.append(ical_event.get('summary'))

      if self.space is None:
        space = self.guess_space(ical_event.get('location', ''))
      else:
        space = self.space

      start = self.convert_datetime(ical_event.get('dtstart').dt, space)
      start_dates.append(timezone.make_naive(start, pytz.utc))

    # Dynamically build 'or' filters
    filter_titles = reduce(lambda q, e: q|Q(title=e.title), titles, Q())
    filter_start_dates = reduce(lambda q, date: q|Q(start=date), start_dates, Q())

    return Event.objects.filter(filter_titles|filter_start_dates)

  def is_duplicate(self, duplicate_candidate, start, title, space):
    """ 
    Determine if the event given as the first argument is a duplicate
    of another event that we are importing by comparing its properties
    """

    e = duplicate_candidate

    # Dates coming from the database are always timezone aware because 
    # settings.USE_TZ is True, so we must convert to a naive datetime in order
    # to compare them.
    naive_start_date = timezone.make_naive(e.start, pytz.utc).date()

    # Start dates and titles and spaces must be identical
    if naive_start_date == start.date() and e.title == title and space == e.space:
      return True

    return False

  def get_recurrence(self, ical_event, event):
    if not ical_event.get('RRULE') \
    and not ical_event.get('EXRULE') \
    and not ical_event.get('RDATE') \
    and not ical_event.get('EXDATE'):
      return None

    def get_as_list(obj, attr):
      v = obj.get(attr)
      if v:
        return v if isinstance(v, list) else [v]
      return []

    def to_utc(dt):
      if timezone.is_aware(dt):
        return timezone.make_naive(dt.astimezone(pytz.utc), pytz.utc)
      else:
        return pytz.utc.localize(dt)

    rset = rruleset()

    for rrule in get_as_list(ical_event, 'RRULE'):
      rrule = rrulestr(rrule.to_ical(), dtstart=event.start)
      rset.rrule(rrule)

    for exrule in get_as_list(ical_event, 'EXRULE'):
      exrule = rrulestr(exrule.to_ical(), dtstart=event.start)
      rset.rrule(exrule)

    for rdate in get_as_list(ical_event, 'RDATE'):
      for dt in rdate.dts:
        rset.rdate(to_utc(dt.dt))

    for exdate in get_as_list(ical_event, 'EXDATE'):
      for dt in exdate.dts:
        rset.exdate(to_utc(dt.dt))

    return from_dateutil_rruleset(rset)
