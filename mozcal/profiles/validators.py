import datetime

from django.core.exceptions import ValidationError
from django.utils import timezone

def _validate_birth_date(data, **kwargs):
  """
  Validator to ensure age of at least 12 years old.
  """
  today = timezone.now().date()
  youth_threshold_day = (datetime.date(today.year - 12, today.month,
                                       today.day) +
                         datetime.timedelta(hours=24))

  if data > youth_threshold_day:
    raise ValidationError('Provided Birthdate is not valid.')

  return data
