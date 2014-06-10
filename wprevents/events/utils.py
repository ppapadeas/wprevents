def add_filter(dict, field, filter, value):
  '''Conditionally add a filter to a dict if value is set'''
  if value:
    dict['{0}__{1}'.format(field, filter)] = value
