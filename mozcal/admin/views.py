from django.shortcuts import render, get_object_or_404

from mozcal.events.models import Event, Space


def events_list(request):
  events = Event.objects.all()

  return render(request, 'events.html', { 'events': events })


def event_edit(request, id):
  event = get_object_or_404(Event, id=id)

  return render(request, 'edit_event.html', { 'event': event })


def space_edit(request, id):
  space = get_object_or_404(Space, id=id)

  return render(request, 'edit_space.html', { 'space': space })