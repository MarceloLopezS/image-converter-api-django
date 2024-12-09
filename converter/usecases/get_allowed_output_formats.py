def get_allowed_output_formats(output_format_model):
  def inner():
    return list(
      output_format_model.objects.values_list("name", flat=True)
    )
  
  return inner