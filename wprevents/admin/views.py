from django.contrib.auth.decorators import permission_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render

from wprevents.base.utils import get_or_create_instance, save_ajax_form
from wprevents.base.decorators import json_view, ajax_required
from wprevents.events.models import Event, Space, FunctionalArea

from forms import EventForm, SpaceForm, FunctionalAreaForm, ImportEventForm
import import_ical


# EVENTS

@permission_required('events.can_administrate_events')
def events_list(request):
  order_by = request.GET.get('order_by', '-start')

  event_list = Event.objects.all().order_by(order_by).select_related('space').prefetch_related('areas')
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
    page = paginator.num_pages
    events = paginator.page(page)

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
    return save_ajax_form(form)

  return render(request, 'event_modal.html', { 'event': event, 'form': form })


@permission_required('events.can_administrate_events')
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
def event_dedupe(request, id=None):
  event = Event.objects.get(id=id)

  if request.method == 'POST':
    event.remove_duplicate(request.POST.get('duplicate_id'))
    return HttpResponseRedirect(reverse('event_dedupe', args=[event.id]))

  events = event.get_duplicate_candidates(request.GET.get('q', ''))

  return render(request, 'event_dedupe.html', {
    'event': event,
    'events': events
  })


@permission_required('events.can_administrate_events')
@ajax_required
@json_view
def event_import_ical(request):
  form = ImportEventForm(request.POST or None)

  if form.is_valid():
    url = form.cleaned_data['url']
    file = form.cleaned_data['file']

    if not url and not file:
      return { 'status': 'error', 'errors': { '1': 'Import field cannot be empty' } }

    try:
      if url:
        imported_events = import_ical.from_url(url)

      if file:
        imported_events = import_ical.from_file(file)

    except import_ical.Error as e:
      return { 'status': 'error', 'errors': { '1': str(e) } }
    except Exception, e:
      return { 'status': 'error', 'errors': { '1': str(e) } }

    message = 'Successfully imported ' + str(len(imported_events)) + ' events'
    return {
      'status': 'success',
      'message': message
    }

  return render(request, 'import_modal.html')


# SPACES

@permission_required('events.can_administrate_spaces')
def spaces_list(request):
  order_by = request.GET.get('order_by', 'name')
  spaces = Space.objects.all().order_by(order_by)

  return render(request, 'spaces.html', { 'spaces': spaces })


@permission_required('events.can_administrate_spaces')
@ajax_required
@json_view
def space_edit(request, id=None):
  id = request.POST.get('id') or id
  space, created = get_or_create_instance(Space, id=id)
  form = SpaceForm(request.POST or None, request.FILES or None, instance=space)

  if request.method == 'POST':
    return save_ajax_form(form)

  return render(request, 'space_modal.html', { 'space': space, 'form': form })


@permission_required('events.can_administrate_spaces')
def space_delete(request):
  space = Space.objects.get(id=request.POST.get('id'))

  if space:
    space.delete()

  return HttpResponseRedirect(reverse('space_all'))


# AREAS

@permission_required('events.can_administrate_functional_areas')
def area_list(request):
  order_by = request.GET.get('order_by', 'name')
  areas = FunctionalArea.objects.all().order_by(order_by)

  return render(request, 'areas.html', { 'areas': areas })


@permission_required('events.can_administrate_functional_areas')
@ajax_required
@json_view
def area_edit(request, id=None):
  id = request.POST.get('id') or id
  area, created = get_or_create_instance(FunctionalArea, id=id)
  form = FunctionalAreaForm(request.POST or None, instance=area)

  if request.method == 'POST':
    return save_ajax_form(form)

  return render(request, 'area_modal.html', { 'area': area, 'form': form })


@permission_required('events.can_administrate_functional_areas')
def area_delete(request):
  area = FunctionalArea.objects.get(id=request.POST.get('id'))
  area.delete()

  return HttpResponseRedirect(reverse('area_all'))
