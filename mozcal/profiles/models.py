from django.contrib.auth.models import User
from django.db import models

from .validators import _validate_birth_date


class UserProfile(models.Model):
  user = models.OneToOneField(User)
  birth_date = models.DateField(validators=[_validate_birth_date],
                                blank=True, null=True)
  city = models.CharField(max_length=50, blank=False, default='')
  region = models.CharField(max_length=50, blank=False, default='')
  country = models.CharField(max_length=50, blank=False, default='')
  lon = models.FloatField(blank=False, null=True)
  lat = models.FloatField(blank=False, null=True)
