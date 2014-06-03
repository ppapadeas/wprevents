def get_or_create_instance(model_class, **kwargs):
  """
  Identical to get_or_create, expect instead of saving the new
  object in the database, this just creates an instance.
  """
  try:
    return model_class.objects.get(**kwargs), False
  except model_class.DoesNotExist:
    return model_class(**kwargs), True

def save_ajax_form(form):
  if form.is_valid():
    form.save()
    return { 'status': 'success' }
  else:
    return { 'status': 'error',
             'errors': dict(form.errors.iteritems()) }