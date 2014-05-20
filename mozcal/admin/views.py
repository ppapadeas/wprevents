from django.shortcuts import render
from django.http import HttpResponseRedirect

from mozcal.base.utils import get_or_create_instance
from mozcal.events.models import Event, Space

from .forms import EventForm, SpaceForm
from .utils import as_csv

def events_list(request):
  events = Event.objects.all()

  if request.GET.get('format') == 'csv':
    return as_csv(request, Event.objects.all(), ['title', 'space', 'start', 'end', 'area_names'], fileName='events.csv')

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


def event_dedupe(request, slug=None):
  event = Event.objects.get(slug=slug)

  if request.method == 'POST':
    event.remove_duplicate(request.POST.get('duplicate_id'))
    return HttpResponseRedirect('/admin/events/'+ event.slug +'/dedupe')

  events = event.get_duplicate_candidates(request.GET.get('q'))

  return render(request, 'event_dedupe.html', { 'events': events })


def spaces_list(request):
  spaces = Space.objects.all()

  if request.GET.get('format') == 'csv':
    return as_csv(request, Space.objects.all(), ['name', 'address', 'address2', 'city', 'country', 'lat', 'lon', 'photo_url'], fileName='spaces.csv')

  return render(request, 'spaces.html', { 'spaces': spaces })


def space_edit(request, slug=None):
  space, created = get_or_create_instance(Space, slug=slug)
  form = SpaceForm(request.POST or None, instance=space)

  if request.method == 'POST':
    if form.is_valid():
      form.save()
      return HttpResponseRedirect('/admin/spaces')

  return render(request, 'space_form.html', { 'space': space, 'form': form })

def space_delete(request):
  space = Space.objects.get(id=request.POST.get('id'))

  space.delete()
  return HttpResponseRedirect('/admin/spaces')
