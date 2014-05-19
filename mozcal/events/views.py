from django.shortcuts import render, get_object_or_404

from mozcal.events.models import Event

def one(request, slug):
  event = get_object_or_404(Event, slug=slug)

  return render(request, 'event.html', { 'event': event })


def all(request):
  events = Event.objects.all()

  return render(request, 'events_all.html', { 'events': events })
