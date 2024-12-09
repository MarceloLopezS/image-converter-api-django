def is_file_extension_allowed(filename, allowed_list):
    if not filename:
        return False
    if len(filename) == 0:
        return False
    
    return "." in filename and \
        filename.rsplit(".", 1)[1].lower() in allowed_list


def is_output_format_allowed(output_format, allowed_list):
    if not output_format or len(output_format) == 0:
        return False
    
    return output_format in allowed_list


def are_valid_output_params(
  output_format,
  output_params,
  allowed_output_params
):
    if not output_format or len(output_format) == 0:
        return False
    
    if not output_params or len(output_params) == 0:
        return False
    
    for param_name in output_params:
        if param_name not in allowed_output_params:
            return False
        
    return True