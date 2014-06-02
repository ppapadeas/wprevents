from django.contrib.auth.decorators import permission_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect
from django.shortcuts import render

from wprevents.base.utils import get_or_create_instance
from wprevents.base.decorators import json_view, ajax_required
from wprevents.events.models import Event, Space, FunctionalArea

from .forms import EventForm, SpaceForm, FunctionalAreaForm
import import_ical


@permission_required('events.can_administrate_events')
def home(request):
  return render(request, 'admin.html')


# EVENTS

@permission_required('events.can_administrate_events')
def events_list(request):
  order_by = request.GET.get('order_by', '-start')

  event_list = Event.objects.all().order_by(order_by)
  paginator = Paginator(event_list, 20) # Mockup/spec: 22 items per page

  page = request.GET.get('page')

  try:
    events = paginator.page(page)
  except PageNotAnInteger:
    # If page is not an integer, deliver first page.
    page = 1
    events = paginator.page(page)
  except EmptyPage:
    # If page is out of range (e.g. 9999), deliver last page of results.
    events = paginator.page(paginator.num_pages)

  return render(request, 'events.html', {
    'events': events,
    'paginator': events.paginator,
    'current_page': int(page),
    'order_by': order_by
  })


@permission_required('events.can_administrate_events')
@ajax_required
@json_view
def event_edit(request, id=None):
  id = request.POST.get('id') or id
  event, created = get_or_create_instance(Event, id=id)
  form = EventForm(request.POST or None, instance=event)

  if request.method == 'POST':
    if form.is_valid():
      form.save()
      return { 'status': 'success' }
    else:
      return { 'status': 'error',
               'errors': dict(form.errors.iteritems()) }

  return render(request, 'event_form.html', { 'event': event, 'form': form })



@permission_required('events.can_administrate_events')
@ajax_required
@json_view
def event_delete(request):
  event = Event.objects.get(id=request.POST.get('id'))

  if event:
    event.delete()

  query_string = request.META.get('QUERY_STRING', '')
  query_string = '?' + query_string if query_string else ''
  redirect_to = '/admin/events/' + query_string

  return HttpResponseRedirect(redirect_to)


@permission_required('events.can_administrate_events')
@ajax_required
@json_view
def event_dedupe(request, id=None):
  event = Event.objects.get(id=id)

  if request.method == 'POST':
    event.remove_duplicate(request.POST.get('duplicate_id'))
    return HttpResponseRedirect('/admin/events/'+ event.id +'/dedupe')

  events = event.get_duplicate_candidates(request.GET.get('q', ''))

  return render(request, 'event_dedupe.html', {
    'event': event,
    'events': events
  })

@permission_required('events.can_administrate_events')
def event_import_ical(request):
  if request.method == 'POST':
    error = ''

    try:
      url = request.POST.get('url')
      cal_file = request.FILES.get('file', None)
      source = ''
      events = []

      if url:
        events = import_ical.from_url(url)
        source = url

      if cal_file:
        events = import_ical.from_file(cal_file)
        source = cal_file

      return render(request, 'event_import.html', {
        'events': events,
        'source': source
      })
    except import_ical.Error as e:
      error = e;

    return render(request, 'event_import.html', { 'error': error })

  return render(request, 'event_import.html')


# SPACES

@permission_required('events.can_administrate_spaces')
def spaces_list(request):
  order_by = request.GET.get('order_by', 'name')
  spaces = Space.objects.all().order_by(order_by)

  return render(request, 'spaces.html', { 'spaces': spaces })

@permission_required('events.can_administrate_spaces')
def space_edit(request, id=None):
  space, created = get_or_create_instance(Space, id=id)
  form = SpaceForm(request.POST or None, instance=space)

  if request.method == 'POST':
    if form.is_valid():
      form.save()
      return HttpResponseRedirect('/admin/spaces')

  return render(request, 'space_form.html', { 'space': space, 'form': form })

@permission_required('events.can_administrate_spaces')
def space_delete(request):
  space = Space.objects.get(id=request.POST.get('id'))

  if space:
    space.delete()

  return HttpResponseRedirect('/admin/spaces')


# AREAS

@permission_required('events.can_administrate_functional_areas')
def area_list(request):
  order_by = request.GET.get('order_by', 'name')
  areas = FunctionalArea.objects.all().order_by(order_by)

  return render(request, 'areas.html', { 'areas': areas })

@permission_required('events.can_administrate_functional_areas')
def area_edit(request, id=None):
  area, created = get_or_create_instance(FunctionalArea, id=id)
  form = FunctionalAreaForm(request.POST or None, instance=area)

  if request.method == 'POST':
    if form.is_valid():
      form.save()
      return HttpResponseRedirect('/admin/areas')

  return render(request, 'area_form.html', { 'area': area, 'form': form })

@permission_required('events.can_administrate_functional_areas')
def area_delete(request):
  area = FunctionalArea.objects.get(id=request.POST.get('id'))

  area.delete()
  return HttpResponseRedirect('/admin/area')
