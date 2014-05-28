import csv

from django.http import HttpResponse


def as_csv(request, queryset, fields, fileName='export.csv'):
  response = HttpResponse(mimetype='text/csv')
  response['Content-Disposition'] = 'attachment;filename=' + fileName

  writer = csv.writer(response)
  writer.writerow([field for field in fields])
  for obj in queryset:
    writer.writerow([getattr(obj, field) for field in fields])

  return response
