import os

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


def delete_empty_dirs(base_path):
    for root, dirs, files in os.walk(base_path, topdown=False):
        for dir in dirs:
            full_path = os.path.join(root, dir)
            try:
                if not os.listdir(full_path):  # Check if directory is empty
                    os.rmdir(full_path)
            except Exception as e:
                print(f"Error removing directory {full_path}: {e}")