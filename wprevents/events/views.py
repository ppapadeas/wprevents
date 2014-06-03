from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from wprevents.base.decorators import ajax_required, post_required
from wprevents.events.models import Event, Space, FunctionalArea
from wprevents.events.forms import SearchForm

from month_manager import MonthManager
from utils import sanitize_calendar_input


def one(request, id, slug):
  event = get_object_or_404(Event, id=id)

  return render(request, 'event.html', { 'event': event })


def all(request):
  search_string = request.GET.get('search', '')
  space_name = request.GET.get('space', '')
  area_name = request.GET.get('area', '')

  events = Event.objects.all()

  spaces = Space.objects.all()
  areas = FunctionalArea.objects.all()

  return render(request, 'list.html', {
    'events': events,
    'spaces': spaces,
    'areas': areas
  })


@ajax_required
def search(request):
  form = SearchForm(request.GET)
  events = []

  if form.is_valid():
    # TODO: also filter by start date, end date
    events = Event.objects.search(form.cleaned_data['space'],
                                  form.cleaned_data['area'],
                                  form.cleaned_data['keyword'])

  return render(request, 'list_content.html', {
    'events': events
  })


def calendar(request):
  now = timezone.now()

  year, month = sanitize_calendar_input(
    request.GET.get('year', now.year),
    request.GET.get('month', now.month),
    now
  )

  events = Event.objects.filter(start__year=year, start__month=month)
  month_manager = MonthManager(year=year, month=month, events=events)

  return render(request, 'calendar.html', {
    'month_manager': month_manager
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
