def get_allowed_io(input_file_extension_model, output_format_model):
    def inner(max_file_size_bytes):
        file_extensions = \
          list(
              input_file_extension_model.objects.order_by("name")\
                .values_list("name", flat=True)
          )
        file_formats = \
          list(
              output_format_model.objects.order_by("name")\
                .values_list("name", flat=True)
          )
        
        return {
            "input": {
                "file_extensions": file_extensions,
                "max_file_size_bytes": max_file_size_bytes
            },
            "output": {
                "file_formats": file_formats
            }
        }
    
    return inner