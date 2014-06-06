from django.conf import settings

from jingo import register
import jinja2


LINE_LIMIT = 75
FOLD_SEP = u'\r\n '


@register.filter
def format_datetime_utc(obj):
  """Return datetime object UTC formatted."""
  return obj.strftime('%Y%m%dT%H%M%S')


@register.filter
def ical_escape_char(text):
  """Escape characters as defined in RFC5545.

  Original code from https://github.com/collective/icalendar
  Altered by John Giannelos <jgiannelos@mozilla.com>

  """
  return (text.replace('\N', '\n')
              .replace('\\', '\\\\')
              .replace(';', r'\;')
              .replace(',', r'\,')
              .replace('\r\n', r'\n')
              .replace('\n', r'\n'))


@register.filter
def ical_format_lines(text):
  """Make a string folded as defined in RFC5545.

  Original code from https://github.com/collective/icalendar
  Altered by John Giannelos <jgiannelos@mozilla.com>

  """
  ret_line = u''
  byte_count = 0

  for char in text:
    char_byte_len = len(char.encode('utf-8'))
    byte_count += char_byte_len

    if byte_count >= LINE_LIMIT:
      ret_line += FOLD_SEP
      byte_count = char_byte_len
    ret_line += char

  return ret_line


@register.filter
def media_path(filename):
  return settings.MEDIA_URL + filename if filename else ''


@register.function
@register.inclusion_tag('paginator.html')
@jinja2.contextfunction
def show_paginator(context, adjacent_pages=2, order_by=None):
  '''
  Based on http://www.tummy.com/articles/django-pagination/
  '''
  paginator = context['paginator']
  current_page = context['current_page']
  total_pages = paginator.num_pages

  start_page = max(current_page - adjacent_pages, 1)
  if start_page <= 3:
    start_page = 1

  end_page = current_page + adjacent_pages + 1

  if end_page >= total_pages - 1:
    end_page = total_pages + 1

  page_numbers = [n for n in range(start_page, end_page) if n > 0 and n <= total_pages]

  previous_page = current_page - 1
  next_page = current_page + 1

  total_pages = paginator.page_range[-1]

  return {
    'page_obj': paginator.page,
    'paginator': paginator,
    'results_per_page': paginator.per_page,
    'current_page': current_page,
    'total_pages': paginator.page_range[-1],
    'page_numbers': page_numbers,
    'previous': previous_page,
    'next': next_page,
    'has_next': current_page < total_pages,
    'has_previous': previous_page > 0,
    'show_first': 1 not in page_numbers,
    'show_last': total_pages not in page_numbers,
    'order_by': order_by
  }
