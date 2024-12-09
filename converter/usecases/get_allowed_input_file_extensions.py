def get_allowed_input_file_extensions(input_file_extension_model):
    def inner():
        return list(
            input_file_extension_model.objects.values_list("name", flat=True)
        )
    
    return inner