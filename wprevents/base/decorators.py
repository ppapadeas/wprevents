import json

from functools import wraps

from django.http import (HttpResponse, HttpResponseNotAllowed,
                         HttpResponseBadRequest)


def ajax_required(f):
  def wrap(request, *args, **kwargs):
      if not request.is_ajax():
        return HttpResponseBadRequest()
      return f(request, *args, **kwargs)
  wrap.__doc__=f.__doc__
  wrap.__name__=f.__name__
  return wrap


def post_required(f):
  @wraps(f)
  def wrapper(request, *args, **kw):
    if request.method != 'POST':
      return HttpResponseNotAllowed(['POST'])
    else:
      return f(request, *args, **kw)
  return wrapper


def json_view(f):
  @wraps(f)
  def wrapper(*args, **kw):
    response = f(*args, **kw)
    if isinstance(response, HttpResponse):
      return response
    else:
      return HttpResponse(json.dumps(response),
                  content_type='application/json')
  return wrapper

json_view.error = lambda s: http.HttpResponseBadRequest(
  json.dumps(s), content_type='application/json')


