from django.http import HttpResponseServerError
from django.shortcuts import render
from django.template import RequestContext
from django.template.loader import get_template


def login(request):
  return render(request, 'login.html')


def error404(request):
  t = get_template('404.html')
  res = HttpResponseServerError(t.render(RequestContext(request)))

  return res


def error500(request):
  t = get_template('500.html')
  res = HttpResponseServerError(t.render(RequestContext(request)))

  return res
