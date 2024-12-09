def get_output_format_param_fields(output_format_model):
  def inner(output_format):
    output_param_fields = output_format_model.objects.get(
      name=output_format
    ).get_output_param_fields()

    return output_param_fields
  
  return inner