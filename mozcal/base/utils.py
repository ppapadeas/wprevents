from datetime import datetime


def get_or_create_instance(model_class, **kwargs):
  """
  Identical to get_or_create, expect instead of saving the new
  object in the database, this just creates an instance.
  """
  try:
    return model_class.objects.get(**kwargs), False
  except model_class.DoesNotExist:
    return model_class(**kwargs), True

def validate_datetime(data, **kwargs):
  """Validate that /data/ is of type datetime.

  Used to validate DateTime form fields, to ensure that user select
  a valid date, thus a date that can be converted to a datetime
  obj. Example of invalid date is 'Sept 31 2012'.

  """

  if not isinstance(data, datetime):
      raise ValidationError('Date chosen is invalid.')
  return data