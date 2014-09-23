from datetime import datetime

from dateutil.relativedelta import relativedelta
from django.db import connection, transaction

from wprevents.events.models import Event, Instance

from celery.task import task


@task
@transaction.commit_manually
def generate_event_instances():  
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

  # Populate temporary table with new instances
  old_table = Instance._meta.db_table;
  new_table = old_table + '_new';
  tmp_table = old_table + '_tmp';

  cursor = connection.cursor()

  try:
    cursor.execute('CREATE TABLE %s LIKE %s;' % (new_table, old_table))

    for i in instances:
      id = i.event.id
      start = i.start.strftime('%Y-%m-%d %H:%M:%S')
      end = i.end.strftime('%Y-%m-%d %H:%M:%S')
      sql = "INSERT INTO %s (event_id, start, end) VALUES ('%s', '%s', '%s');" % (new_table, id, start, end)
      cursor.execute(sql)

    # Swap instance tables
    cursor.execute('RENAME TABLE %s TO %s, %s TO %s;' % (old_table, tmp_table, new_table, old_table))
    cursor.execute('DROP TABLE %s;' % tmp_table)

  finally:
    cursor.close()

  transaction.commit()
