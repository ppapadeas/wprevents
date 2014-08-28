from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.http import HttpResponse

from wprevents.base.decorators import ajax_required, json_view
from wprevents.events.models import Event, Space, FunctionalArea
from wprevents.events.forms import SearchForm

from datetime import datetime

from month_manager import MonthManager


def one(request, id, slug):
  event = get_object_or_404(Event.objects.select_related('space').prefetch_related('areas'), id=id)

  return render(request, 'event.html', {
    'event': event,
    'event_absolute_url': request.build_absolute_uri(reverse('events_event_single', args=(event.pk, event.slug,)))
  })


def render_index(request, template):
  list_events = Event.objects.upcoming_events().order_by('start')
  list_events = list_events.select_related('space').prefetch_related('areas')

  now = timezone.now()
  calendar_events = Event.objects.of_given_month(now.year, now.month)
  calendar_events = calendar_events.select_related('space').prefetch_related('areas')
  month_manager = MonthManager(year=now.year, month=now.month, events=calendar_events)

  return render(request, template, {
    'list_events': list_events,
    'spaces': Space.objects.all(),
    'areas': FunctionalArea.objects.all(),
    'month_manager': month_manager
  })

def list(request):
  return render_index(request, 'list.html')

def calendar(request):
  return render_index(request, 'calendar.html')


@ajax_required
def filter_list(request):
  form = SearchForm(request.GET)
  events = []

  if form.is_valid():
    search_params = {
      'space_name': form.cleaned_data['space'],
      'area_name': form.cleaned_data['area'],
      'search_string': form.cleaned_data['keyword'],
      'start_date': form.cleaned_data.get('start'),
      'end_date': form.cleaned_data.get('end')
    }

    events = Event.objects.search(**search_params).order_by('start')

  return render(request, 'list_content.html', {
    'list_events': events
  })


@ajax_required
def filter_calendar(request):
  form = SearchForm(request.GET)
  now = timezone.now()

  if form.is_valid():
    search_params = {
      'space_name': form.cleaned_data['space'],
      'area_name': form.cleaned_data['area'],
      'search_string': form.cleaned_data['keyword'],
      'year': form.cleaned_data.get('year', now.year),
      'month': form.cleaned_data.get('month', now.month)
    }

    calendar_events = Event.objects.search(**search_params)
    month_manager = MonthManager(year=search_params['year'], month=search_params['month'], events=calendar_events)

  return render(request, 'calendar_content.html', {
    'month_manager': month_manager
  })


def screen(request, slug):
  events = Event.objects.upcoming_events().filter(space__slug=slug).order_by('start')[:10]

  return render(request, 'screen.html', {
    'list_events': events
  })


@ajax_required
def map_spaces(request):
  response = render(request, 'spaces.json', {
    'spaces': Space.objects.all()
  })

  return HttpResponse(response.content, content_type='application/json')


def test_import2(request):
  from wprevents.admin.event_importer import EventImporter

  importer = EventImporter()

  with open("tmp/test.ics", "r") as ics_file:
    data = ics_file.read().decode('utf-8')

  importer.from_string(data)

  return HttpResponse(datetime.now())


def test_import(request):
  from datetime import datetime

  e = Event.objects.all()[0]

  # print(e.recurrence.count())
  events = e.get_instances(after=datetime(2013, 8, 6, 0, 0), before=datetime.now())

  print(events)

  return HttpResponse(datetime.now())
