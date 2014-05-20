from django.shortcuts import render, get_object_or_404

from mozcal.events.models import Event, Space, FunctionalArea

def one(request, slug):
  event = get_object_or_404(Event, slug=slug)

  return render(request, 'event.html', { 'event': event })


def all(request):
  search_string = request.GET.get('search', '')
  space_name = request.GET.get('space', '')
  area_name = request.GET.get('area', '')

  events = Event.objects.filter(title__icontains=search_string).filter(space__slug__contains=space_name).filter(areas__slug__contains=area_name)
  spaces = Space.objects.all()
  areas = FunctionalArea.objects.all()

  return render(request, 'events_all.html', {
    'events': events,
    'spaces': spaces,
    'areas': areas
  })