from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.views.decorators.csrf import csrf_exempt

from wprevents.base.decorators import post_required, ajax_required, json_view
from wprevents.events.models import Event, Instance, Space, FunctionalArea
from wprevents.events.forms import SearchForm

from datetime import datetime

from month_manager import MonthManager


def one(request, id, start, slug):
  start = datetime.strptime(start, '%Y%m%d%H%M%S')
  instance = Instance.objects.filter(event_id=id).filter(start=start)

  if not instance:
    raise Http404

  instance = instance[0]

  return render(request, 'event.html', {
    'instance': instance,
    'event_absolute_url': request.build_absolute_uri(reverse('events_event_single', args=(instance.event.id, instance.start_str, instance.event.slug,)))
  })


def render_index(request, template):
  list_instances = Instance.objects.upcoming().order_by('start')
  list_instances = list_instances.select_related('event__space').prefetch_related('event__areas')

  now = timezone.now()
  calendar_instances = Instance.objects.of_given_month(now.year, now.month)
  calendar_instances = calendar_instances.select_related('event__space').prefetch_related('event__areas')
  month_manager = MonthManager(year=now.year, month=now.month, instances=calendar_instances)

  return render(request, template, {
    'list_instances': list_instances,
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
  instances = []

  if form.is_valid():
    search_params = {
      'space_name': form.cleaned_data['space'],
      'area_name': form.cleaned_data['area'],
      'search_string': form.cleaned_data['keyword'],
      'start_date': form.cleaned_data.get('start'),
      'end_date': form.cleaned_data.get('end')
    }

    instances = Instance.objects.search(**search_params).order_by('start')

  return render(request, 'list_content.html', {
    'list_instances': instances
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

    calendar_instances = Instance.objects.search(**search_params)
    month_manager = MonthManager(year=search_params['year'], month=search_params['month'], instances=calendar_instances)

  return render(request, 'calendar_content.html', {
    'month_manager': month_manager
  })


def screen(request, slug):
  instances = Instance.objects.upcoming().filter(event__space__slug=slug).order_by('start')[:10]

  return render(request, 'screen.html', {
    'list_instances': instances,
    'space': instances[0].event.space.slug if len(instances) > 0 else ''
  })


@ajax_required
def map_spaces(request):
  response = render(request, 'spaces.json', {
    'spaces': Space.objects.all()
  })

  return HttpResponse(response.content, content_type='application/json')


def event_redirect_url(request, id):
  e = Event.objects.get(pk=id)

  if not e:
    return Http404()

  return HttpResponseRedirect(e.url)

@post_required
@csrf_exempt
def test_import(request):
  from wprevents.admin.event_importer import EventImporter

  s = Space.objects.get(slug='portland')
  importer = EventImporter(s)

  with open("tmp/MOZPORTLAND.ics", "r") as ics_file:
    data = ics_file.read().decode('utf-8')

  importer.from_string(data)

  return HttpResponse(datetime.now())


@post_required
@csrf_exempt
def test_import2(request):
  from datetime import datetime

  e = Event.objects.all()[0]

  # print(e.recurrence.count())
  events = e.get_instances(after=datetime(2013, 8, 6, 0, 0), before=datetime.now())

  print(events)

  return HttpResponse(datetime.now())
