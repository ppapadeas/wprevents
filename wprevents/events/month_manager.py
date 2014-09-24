import calendar
from datetime import date, time


class MonthManager(object):
  def __init__(self, year, month, instances):
    self.matrix = calendar.monthcalendar(year, month)
    self.instances = instances
    self.name = calendar.month_name[month]
    self.month = month
    self.year = year

  def get_instances_for_day(self, day):
    day = date(self.year, self.month, day)
    day_instances = []

    for i in self.instances:
      if i.start.date() <= day <= i.end.date():
        if day == i.end.date() and i.end.time() == time(0, 0, 0):
          # All-day events finish at 00:00 on their end date, but we don't want them
          # to appear in the calendar on this date because they could be mistaken for
          # multi-day events. This is why we need to handle this special case here.
          continue
        day_instances.append(i)

    return day_instances

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

  def format_date_for_day(self, day):
    return date(self.year, self.month, day)
