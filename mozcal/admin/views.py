from django.shortcuts import render, get_object_or_404

from mozcal.events.models import Event


def events_list(request):
  events = Event.objects.all()

  return render(request, 'events.html', { 'events': events })


def event_edit(request, id):
  event = get_object_or_404(Event, id=id)

  return render(request, 'edit_event.html', { 'event': event })