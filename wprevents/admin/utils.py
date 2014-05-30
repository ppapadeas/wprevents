import urllib2

from icalendar import Calendar

from wprevents.events.models import Event


def import_ical(url):
  request = urllib2.Request(url)
  response = urllib2.urlopen(request)

  data = response.read().decode('utf-8')

  data = data.replace(u"", "") # Temp fix for Mozilla remo ics file

  cal = Calendar.from_ical(data)

  for event in cal.walk('VEVENT'):
    model = Event(title="foo")
    model.start = event.get('dtstart').dt
    model.end = event.get('dtend').dt
    model.title = event.get('summary')
    model.description = event.get('description')

  return