from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from wprevents.events.models import Event, Space, FunctionalArea
from month_manager import MonthManager


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


def calendar(request):
  now = timezone.now()

  try:
    year = int(request.GET.get('year', now.year))
    month = int(request.GET.get('month', now.month))
  except ValueError:
    year = now.year
    month = now.month

  month = sorted((1, month, 12))[1] # Clamp month into 1..12 range

  events = Event.objects.filter(start__year=year, start__month=month)
  month_manager = MonthManager(year=year, month=month, events=events)

  return render(request, 'calendar.html', {
    'month_manager': month_manager
  })