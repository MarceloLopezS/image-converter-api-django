def convert_image(image_converter_model):
    def inner(input_image, output_image_path, output_format, **kwargs):
        return image_converter_model.convert(
            input_image,
            output_image_path,
            output_format,
            **kwargs
        )
    
    return inner