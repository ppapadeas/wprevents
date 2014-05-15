from django.shortcuts import render

from mozcal.events.models import Event

def events_list(request):
  events = Event.objects.all()

  return render(request, 'events.html', { 'events': events })
