def convert_image(image_converter_model):
    def inner(
      input_image,
      output_filename,
      output_format,
      expiration_timedelta,
      **kwargs
    ):
        return image_converter_model.convert(
            input_image,
            output_filename,
            output_format,
            expiration_timedelta,
            **kwargs
        )
    
    return inner