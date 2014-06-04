from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from wprevents.base.decorators import ajax_required
from wprevents.events.models import Event, Space, FunctionalArea
from wprevents.events.forms import SearchForm

from month_manager import MonthManager
from utils import sanitize_calendar_input


def one(request, id, slug):
  event = get_object_or_404(Event, id=id)

  return render(request, 'event.html', { 'event': event })


def render_index(request, template):
  search_string = request.GET.get('search', '')
  space_name = request.GET.get('space', '')
  area_name = request.GET.get('area', '')

  spaces = Space.objects.all()
  areas = FunctionalArea.objects.all()

  now = timezone.now()

  year, month = sanitize_calendar_input(
    request.GET.get('year', now.year),
    request.GET.get('month', now.month),
    now
  )

  events = Event.objects.filter(start__year=year, start__month=month).order_by('-start')
  month_manager = MonthManager(year=year, month=month, events=events)

  return render(request, template, {
    'events': events,
    'spaces': spaces,
    'areas': areas,
    'month_manager': month_manager
  })

def list(request):
  return render_index(request, 'list.html')

def calendar(request):
  return render_index(request, 'calendar.html')


@ajax_required
def search(request):
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
    events = Event.objects.search(**search_params)

  return render(request, 'list_content.html', {
    'events': events
  })


def calendar_month(request):
  now = timezone.now()

  year, month = sanitize_calendar_input(
    request.GET.get('year', now.year),
    request.GET.get('month', now.month),
    now
  )

  events = Event.objects.filter(start__year=year, start__month=month)
  month_manager = MonthManager(year=year, month=month, events=events)

  return render(request, 'calendar_content.html', {
    'month_manager': month_manager
  })
