import calendar


class MonthManager(object):
  def __init__(self, year, month, events):
    self.matrix = calendar.monthcalendar(year, month)
    self.events = events
    self.name = calendar.month_name[month]
    self.month = month
    self.year = year

  def get_events_for_day(self, day):
    return [e for e in self.events if e.start.day == day]

  @property
  def previous_month(self):
    previous_month = self.month - 1

    return 12 if previous_month == 0 else previous_month

  @property
  def previous_month_name(self):
    return calendar.month_name[self.previous_month]

  @property
  def year_of_previous_month(self):
    return self.year - 1 if self.previous_month == 12 else self.year

  @property
  def next_month(self):
    next_month = self.month + 1

    return 1 if next_month > 12 else next_month

  @property
  def next_month_name(self):
    return calendar.month_name[self.next_month]

  @property
  def year_of_next_month(self):
    return self.year + 1 if self.next_month == 1 else self.year
