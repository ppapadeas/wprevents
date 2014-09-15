from datetime import datetime

from dateutil.relativedelta import relativedelta
from django.db import connection

from wprevents.events.models import Event, Instance

from celery.task import task


@task
def generate_event_instances():
  # Remove all existing instances
  cursor = connection.cursor()
  try:
    cursor.execute('TRUNCATE %s;' % Instance._meta.db_table)
  finally:
    cursor.close()

  # Retrieve event definitions in order to generate all instances
  events = Event.objects.all()
  instances = []
  before = datetime.now() + relativedelta(years=1)

  unique_events = [e for e in events if not e.recurring]
  recurring_events = [e for e in events if e.recurring]

  for e in unique_events:
    instances.append([e.to_instance()])
  for e in recurring_events:
    # TODO: 
    # Using e.recurrence.dtstart here is not correct because theoretically
    # this recurrent event could have an RDATE older than its DTSTART.
    # Instead, we should determine the oldest datetime in the series,
    # and pass it as the `after` argument.
    instances.append(e.get_instances(after=e.recurrence.dtstart, before=before))

  # Flatten this list of lists
  instances = [item for sublist in instances for item in sublist]

  for i in instances:
    i.save()
