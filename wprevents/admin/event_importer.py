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
from recurrence import *
from dateutil.rrule import rruleset, rrulestr


class Error(Exception):
  pass

class EventImporter:
  def __init__(self, space=None):
    self.space = space

  def from_url(self, url):
    return self.from_string(self.fetch_url(url))

  def from_string(self, data):
    cal = self.parse_data(self.sanitize(data))

    # try:
    events, skipped = self.bulk_create_events(cal)
    # except transaction.TransactionManagementError, e:
    #   transaction.rollback()
    #   raise Error('An error with the database transaction occured while bulk inserting events: ' + str(e))
    # except Exception, e:
    #   raise Error('An error occurred while bulk inserting events: ' + str(e))

    return events, skipped


  def fetch_url(self, url):
    try:
      request = urllib2.Request(url)
      response = urllib2.urlopen(request)
    except urllib2.URLError, e:
      raise Error('URL: error' + str(e.reason))
    except urllib2.HTTPError, e:
      raise Error('HTTP error: ' + str(e.code))

    data = response.read().decode('utf-8')

    return data


  def sanitize(self, data):
    data = data.replace(u"", "") # Temp fix for Mozilla remo ICS file

    return data


  def parse_data(self, data):
    try:
      cal = Calendar.from_ical(data)
    except ValueError:
      raise Error('Error parsing icalendar file. The file may contain invalid characters.')

    return cal

  # @transaction.commit_manually
  def bulk_create_events(self, cal):
    ical_events = [e for e in cal.walk('VEVENT')]
    duplicate_events = self.find_duplicates(ical_events)
    spaces = Space.objects.all()

    # Temporary bulk_id used to fetch back newly created events
    bulk_id = random.randrange(1000000000)

    # Prepare batch create by looping through ical events, filtering out duplicates
    events_to_create = []
    recurrences = []
    skipped = 0
    for ical_event in ical_events:
      title = HTMLParser().unescape(ical_event.get('summary'))
      # Filter out duplicate events
      if any(x.title == title for x in duplicate_events):
        skipped += 1
        continue

      start = self.ensure_timezone_datetime(ical_event.get('dtstart').dt)
      start = timezone.make_naive(start, pytz.timezone(settings.TIME_ZONE))

      end = self.ensure_timezone_datetime(ical_event.get('dtend').dt)
      end = timezone.make_naive(end, pytz.timezone(settings.TIME_ZONE))

      location = ical_event.get('location', '')
      description = ical_event.get('description', '')
      description = HTMLParser().unescape(description).encode('utf-8')

      if self.space is None:
        space = self.guess_space(location, spaces)
      else:
        space = self.space

      title = title[:EVENT_TITLE_LENGTH] # Truncate to avoid potential errors

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

    # transaction.commit()

    return created_events, skipped


  def guess_space(self, location, spaces):
    """
    Guess an existing Space from a string containing a raw event location
    """
    guessed_space = [s for s in spaces if s.name.lower() in location.lower()]

    return guessed_space[0] if guessed_space else None


  def guess_functional_areas(self, description, functional_areas):
    guessed_areas = [a for a in functional_areas if a.name.lower() in description.lower()]

    return guessed_areas


  def ensure_timezone_datetime(self, checked_date):
    if isinstance(checked_date, date) and not isinstance(checked_date, datetime):
      # Cast date as datetime: handle special case where events checked_date date is set for the whole day within the iCal file
      checked_date = datetime.combine(checked_date, time())

      if checked_date.tzinfo is None:
        checked_date = pytz.utc.localize(checked_date)
    return checked_date


  def find_duplicates(self, ical_events):
    """
    Return all events previously added in the database that would be duplicate candidates (ie. same title, same start date) of all events provided in the
      imported ical file.
    """
    titles = []
    start_dates = []

    for ical_event in ical_events:
      titles.append(ical_event.get('summary'))
      start = ical_event.get('dtstart').dt
      start = self.ensure_timezone_datetime(start)

      start_dates.append(timezone.make_naive(start, pytz.timezone(settings.TIME_ZONE)))

    # Dynamically build 'or' filters
    filter_titles = reduce(lambda q, e: q|Q(title=e.title), titles, Q())
    filter_start_dates = reduce(lambda q, date: q|Q(start=date), start_dates, Q())

    return Event.objects.filter(filter_titles|filter_start_dates)


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

    if ical_event.get('RDATE'):
      for dt in ical_event['RDATE'].dts:
        rset.rdate(to_utc(dt.dt))

    if ical_event.get('EXDATE'):
      for dt in ical_event['EXDATE'].dts:
        rset.exdate(to_utc(dt.dt))

    return from_dateutil_rruleset(rset)
