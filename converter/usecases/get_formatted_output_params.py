def get_formatted_output_params(output_format_model):
    """
    Takes unformatted output params from the client and formats their
    boolean and multiple-option values so it can be passed to the 
    image processor.
    """
    def inner(output_format, unformatted_output_params):
        fields = output_format_model.objects.get(
            name=output_format
        ).get_output_param_fields()
        
        formatted_output_params = dict()
        
        for paramName in unformatted_output_params:
            for field in fields:
                # Add field if boolean and True
                if field.get("name") == paramName and field.get("is_bool"):
                    if unformatted_output_params[paramName]:
                      formatted_output_params[paramName] = \
                        unformatted_output_params[paramName]
                # Add converted field option list to tuple
                elif field.get("name") == paramName \
                    and isinstance(field.get("options"), list):
                        formatted_output_params[paramName] = \
                          [tuple(unformatted_output_params[paramName])]
                # Add field
                elif field.get("name") == paramName:
                    formatted_output_params[paramName] = \
                      unformatted_output_params[paramName]
                

        return formatted_output_params
    
    return inner