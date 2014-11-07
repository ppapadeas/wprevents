from dateutil.relativedelta import relativedelta
from datetime import datetime

from django.contrib.auth.decorators import permission_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.db import connections
from django.db.models import Count
from django.utils.timezone import make_aware

from pytz import timezone

from wprevents.base.utils import get_or_create_instance, save_ajax_form
from wprevents.base.decorators import json_view, ajax_required, post_required
from wprevents.events.models import Event, Instance, Space, FunctionalArea
from wprevents.base.tasks import generate_event_instances

from forms import EventForm, SpaceForm, FunctionalAreaForm, ImportEventForm
from event_importer import EventImporter, EventImporterError


# EVENTS

@permission_required('events.can_administrate_events')
def events_list(request):
  order_by = request.GET.get('order_by', '-local_start')

  event_list = Event.objects.all().order_by(order_by).select_related('space').prefetch_related('areas')
  paginator = Paginator(event_list, 20) # Mockup/spec: 22 items per page

  page = request.GET.get('page')

  try:
    events = paginator.page(page)
  except PageNotAnInteger:
    # If page is not an integer, deliver first page.
    page = 1
    events = paginator.page(page)
  except EmptyPage:
    # If page is out of range (e.g. 9999), deliver last page of results.
    page = paginator.num_pages
    events = paginator.page(page)

  return render(request, 'events.html', {
    'events': events,
    'paginator': events.paginator,
    'current_page': int(page),
    'order_by': order_by
  })


@permission_required('events.can_administrate_events')
@ajax_required
@json_view
def event_edit(request, id=None):
  id = request.POST.get('id') or id
  event, created = get_or_create_instance(Event, id=id)
  form = EventForm(request.POST or None, instance=event)

  if request.method == 'POST':
    return save_ajax_form(form)

  return render(request, 'event_modal.html', { 'event': event, 'form': form })


@permission_required('events.can_administrate_events')
@post_required
def event_delete(request):
  Event.objects.delete_by_id(id=request.POST.get('id'))

  query_string = request.META.get('QUERY_STRING', '')
  query_string = '?' + query_string if query_string else ''
  redirect_to = '/admin/events/' + query_string

  generate_event_instances.delay()

  return HttpResponseRedirect(redirect_to)


@permission_required('events.can_administrate_events')
@ajax_required
@post_required
@json_view
def event_ajax_delete(request):
  """This view is used by the event de-duplication modal."""
  try:
    event = Event.objects.get(id=request.POST.get('id'))

    if event:
      event.delete()
      generate_event_instances.delay()
  except Event.DoesNotExist:
    pass

  return { 'status': 'success' }


@permission_required('events.can_administrate_events')
@ajax_required
def event_dedupe(request, id=None):
  try:
    event = Event.objects.get(id=id)
    events = event.get_duplicate_candidates(request.GET.get('q', ''))
  except Event.DoesNotExist:
    events = []

  return render(request, 'event_dedupe.html', {
    'event': event,
    'events': events
  })


@permission_required('events.can_administrate_events')
@ajax_required
@json_view
def event_import_ical(request):
  form = ImportEventForm(request.POST or None)

  if request.method == 'POST':
    if form.is_valid():
      url = form.cleaned_data['url']
      space = form.cleaned_data['space']

      try:
        importer = EventImporter(space)
        imported_events, skipped = importer.from_url(url)

      except EventImporterError as e:
        return { 'status': 'error', 'errors': { '1': str(e) } }
      except Exception, e:
        return { 'status': 'error', 'errors': { '1': str(e) } }

      message = 'Import successful: ' + str(len(imported_events)) + ' events created, '+ str(skipped) +' events skipped'

      return {
        'status': 'success',
        'message': message
      }
    else:
      return { 'status': 'error',
               'errors': dict(form.errors.iteritems()) }

  return render(request, 'import_modal.html', {
    'form': form
  })


@permission_required('events.can_administrate_events')
@ajax_required
@json_view
def event_convert_datetimes(request):
  format = '%Y-%m-%d %H:%M'

  start_string = request.GET['start_date'] + ' ' + request.GET['start_time']
  start = datetime.strptime(start_string, format)

  end_string = request.GET['end_date'] + ' ' + request.GET['end_time']
  end = datetime.strptime(end_string, format)

  current_space_id = request.GET['current_space']
  if current_space_id == '':
    current_tz = timezone('UTC')
  else:
    current_tz = timezone(Space.objects.get(id=current_space_id).timezone)

  new_space_id = request.GET['new_space']
  if new_space_id == '':
    new_tz = timezone('UTC')
  else:
    new_tz = timezone(Space.objects.get(id=new_space_id).timezone)

  start = make_aware(start, current_tz)
  end = make_aware(end, current_tz)

  start = new_tz.normalize(start.astimezone(new_tz))
  end = new_tz.normalize(end.astimezone(new_tz))

  return {
    'start_date': start.strftime('%Y-%m-%d'),
    'start_time': start.strftime('%H:%M'),
    'end_date': end.strftime('%Y-%m-%d'),
    'end_time': end.strftime('%H:%M')
  }


# SPACES

@permission_required('events.can_administrate_spaces')
def spaces_list(request):
  order_by = request.GET.get('order_by', 'name')
  spaces = Space.objects.all().order_by(order_by)

  return render(request, 'spaces.html', { 'spaces': spaces })


@permission_required('events.can_administrate_spaces')
@ajax_required
@json_view
def space_edit(request, id=None):
  id = request.POST.get('id') or id
  space, created = get_or_create_instance(Space, id=id)
  form = SpaceForm(request.POST or None, request.FILES or None, instance=space)

  if request.method == 'POST':
    return save_ajax_form(form)

  return render(request, 'space_modal.html', { 'space': space, 'form': form })


@permission_required('events.can_administrate_spaces')
def space_delete(request):
  Space.objects.delete_by_id(id=request.POST.get('id'))

  return HttpResponseRedirect(reverse('admin_spaces_all'))


# AREAS

@permission_required('events.can_administrate_functional_areas')
def area_list(request):
  order_by = request.GET.get('order_by', 'name')
  areas = FunctionalArea.objects.all().order_by(order_by)

  return render(request, 'areas.html', { 'areas': areas })


@permission_required('events.can_administrate_functional_areas')
@ajax_required
@json_view
def area_edit(request, id=None):
  id = request.POST.get('id') or id
  area, created = get_or_create_instance(FunctionalArea, id=id)
  form = FunctionalAreaForm(request.POST or None, instance=area)

  if request.method == 'POST':
    return save_ajax_form(form)

  return render(request, 'area_modal.html', { 'area': area, 'form': form })


@permission_required('events.can_administrate_functional_areas')
def area_delete(request):
  FunctionalArea.objects.delete_by_id(id=request.POST.get('id'))

  return HttpResponseRedirect(reverse('admin_area_list'))


def get_rows(qs):
  results = []

  extract_month = connections[Instance.objects.db].ops.date_trunc_sql('month', 'events_instance.start')
  rows = qs.extra(select={'month': extract_month}).values('month').annotate(num_events=Count('id'))

  for r in rows:
    results.append((r['month'].strftime('%Y-%m'), str(r['num_events'])))

  return results


def get_month_list():
  months = []
  first = Instance.objects.order_by('start')[0].start.date()
  last = Instance.objects.order_by('-start')[0].start.date()
  current = first

  months.append(first.strftime('%Y-%m'))
  while current < last:
    current = current + relativedelta(months=1)
    months.append(current.strftime('%Y-%m'))

  return months


def to_csv(table):
  csv = ''
  for row in table:
    csv += ','.join(row) + '\n'

  return csv


def metrics(request):
  spaces = Space.objects.all()
  areas = FunctionalArea.objects.all()
  months = get_month_list()
  table = [['0'] * (len(spaces) + len(areas) + 2) for x in xrange(len(months) + 1)]

  # Column names
  table[0][0] = 'Date'
  table[0][1] = 'Total events'

  # `Date` column
  for i, m in enumerate(months):
    table[1 + i][0] = m

  # `Total Events` column
  for date, count in get_rows(Instance.objects):
    table[1 + months.index(date)][1] = count

  # Spaces columns
  offset = 2
  
  for i, s in enumerate(spaces):
    table[0][offset + i] = s.name

  for i, s in enumerate(spaces):
    for date, count in get_rows(Instance.objects.filter(event__space=s)):
      table[1 + months.index(date)][offset + i] = count

  # Areas columns
  offset += len(spaces)

  for i, a in enumerate(areas):
    table[0][offset + i] = a.name

  for i, a in enumerate(areas):
    for date, count in get_rows(Instance.objects.filter(event__areas=a)):
      table[1 + months.index(date)][offset + i] = count

  response = HttpResponse(content=to_csv(table))
  response['Content-Disposition'] = "attachment; filename=metrics.csv"

  return response
