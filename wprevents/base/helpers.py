from django.conf import settings

from jingo import register

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
