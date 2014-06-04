def sanitize_calendar_input(year, month, now):
  try:
    year = int(year)
    month = int(month)
  except ValueError:
    year = now.year
    month = now.month

  month = sorted((1, month, 12))[1] # Clamp month into 1..12 range

  return year, month

def add_filter(dict, field, filter, value):
  '''Conditionally add a filter to a dict if value is set'''
  if value:
    dict['{0}__{1}'.format(field, filter)] = value
