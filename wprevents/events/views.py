from django.shortcuts import render, get_object_or_404

from wprevents.events.models import Event, Space, FunctionalArea

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
  return render(request, 'calendar.html')