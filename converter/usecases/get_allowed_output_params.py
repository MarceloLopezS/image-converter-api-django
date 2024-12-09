def get_allowed_output_params(output_format_model):
  def inner(output_format):
    
    allowed_output_params_fields = list(
      output_format_model.objects.get(name=output_format)\
        .get_output_param_fields()
    )
    allowed_output_params = list(map(
        lambda field: field["name"],
        allowed_output_params_fields
    ))

    return allowed_output_params
  
  return inner