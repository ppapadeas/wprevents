from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect

from mozcal.events.models import Event, Space

from .forms import EventForm, SpaceForm


def events_list(request):
  events = Event.objects.all()

  return render(request, 'events.html', { 'events': events })


#@see https://github.com/mozilla/remo/blob/master/remo/events/views.py#L148
def event_edit(request, id):
  event = get_object_or_404(Event, id=id)
  form = EventForm(request.POST or None, instance=event)

  if request.method == 'POST':
    if form.is_valid():
      form.save()
      return HttpResponseRedirect('/admin/events')

  return render(request, 'edit_event.html', { 'event': event, 'form': form })


def spaces_list(request):
  spaces = Space.objects.all()

  return render(request, 'spaces.html', { 'spaces': spaces })


def space_edit(request, id):
  space = get_object_or_404(Space, id=id)
  form = SpaceForm(request.POST or None, instance=space)

  if request.method == 'POST':
    if form.is_valid():
      form.save()
      return HttpResponseRedirect('/admin/spaces')

  return render(request, 'edit_space.html', { 'space': space, 'form': form })
