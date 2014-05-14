from django.shortcuts import render, get_object_or_404

from mozcal.events.models import Event

def one(request, id):
  event = get_object_or_404(Event, id=id)

  return render(request, 'view_event.html', { 'event': event })


def all(request):
  events = Event.objects.all()

  return render(request, 'list_events.html', { 'events': events })
