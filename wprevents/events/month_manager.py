import calendar


class MonthManager(object):
  def __init__(self, year, month, events):
    self.matrix = calendar.monthcalendar(year, month)
    self.events = events
    self.name = calendar.month_name[month]
    self.year = year

  def get_events_for_day(self, day):
    return [e for e in self.events if e.start.day == day]
