from django.shortcuts import render
from django.http import HttpResponseRedirect

from mozcal.base.utils import get_or_create_instance
from mozcal.events.models import Event, Space

from .forms import EventForm, SpaceForm


def events_list(request):
  events = Event.objects.all()

  return render(request, 'events.html', { 'events': events })


#@see https://github.com/mozilla/remo/blob/master/remo/events/views.py#L148
def event_edit(request, slug=None):
  event, created = get_or_create_instance(Event, slug=slug)
  form = EventForm(request.POST or None, instance=event)

  if request.method == 'POST':
    if form.is_valid():
      form.save()
      return HttpResponseRedirect('/admin/events')

  return render(request, 'event_form.html', { 'event': event, 'form': form })


def event_delete(request):
  event = Event.objects.get(id=request.POST.get('id'))

  event.delete()
  return HttpResponseRedirect('/admin/events')


def spaces_list(request):
  spaces = Space.objects.all()

  return render(request, 'spaces.html', { 'spaces': spaces })


def space_edit(request, slug=None):
  space, created = get_or_create_instance(Space, slug=slug)
  form = SpaceForm(request.POST or None, instance=space)

  if request.method == 'POST':
    if form.is_valid():
      form.save()
      return HttpResponseRedirect('/admin/spaces')

  return render(request, 'space_form.html', { 'space': space, 'form': form })
