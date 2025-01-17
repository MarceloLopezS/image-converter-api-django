from io import BytesIO
import json

from ..utils.functions import \
  is_file_extension_allowed, is_output_format_allowed, are_valid_output_params
from ..utils.constants import DEFAULT_EXPIRATION_TIMEDELTA

class ImageConvertController:
    def __init__(
      self,
      handle_image_convert,
      handle_get_allowed_input_file_extensions,
      handle_get_allowed_output_formats,
      handle_get_allowed_output_params,
      handle_get_formatted_output_params
    ):
        self.__convert_image = handle_image_convert
        self.__get_allowed_input_file_extensions = \
          handle_get_allowed_input_file_extensions
        self.__get_allowed_output_formats = \
          handle_get_allowed_output_formats
        self.__get_allowed_output_params = \
          handle_get_allowed_output_params
        self.__get_formatted_output_params = \
          handle_get_formatted_output_params
    
    def convert(self, request, json_response):
        if "file" not in request.FILES:
          return json_response({
              "status": "fail",
              "data": { "message": "No selected file or files." }
          }, status=400)
    
        file = request.FILES["file"]
        fileConfig = request.POST.get("file_config")

        if not fileConfig or len(fileConfig) == 0:
            return json_response({
                "status": "fail",
                "data": { "message": "No file config found." }
            }, status=400)

        try:
            fileConfig = json.loads(fileConfig)
        except:
            return json_response({
                "status": "fail",
                "data": { "message": "Unable to parse files config." }
            }, status=400)

        if not file or not is_file_extension_allowed(
            file.name, self.__get_allowed_input_file_extensions()
        ):
            return json_response({
                "status": "fail",
                "data": { "message": "One or more files are unsupported." }
            }, status=400)
        
        input_image = BytesIO(file.read())
        output_format = fileConfig["outputFormat"]
        output_params = fileConfig["outputParams"]
        output_filename = f"{file.name.rsplit(".", 1)[0]}.{output_format}"

        if not is_output_format_allowed(
            output_format, self.__get_allowed_output_formats()
        ):
            return json_response({
                "status": "fail",
                "data": { "message", "No output format or not allowed." }
            }, status=400)
        
        if not are_valid_output_params(
          output_format,
          output_params,
          self.__get_allowed_output_params(output_format)
        ):
            return json_response({
                "status": "fail",
                "data": {
                    "message": "One or more output params are invalid."
                }
            }, status=400)
        
        try:
            file_uuid = self.__convert_image(
                input_image,
                output_filename,
                output_format,
                DEFAULT_EXPIRATION_TIMEDELTA,
                **self.__get_formatted_output_params(
                    output_format,
                    output_params
                )
            )

            return json_response({
              "status" : "success",
              "data": { "convertion_id": file_uuid }
            }, status=200)
        except Exception as err:
            print("Convertion error:", err)
            return json_response({
                "status": "fail",
                "data":
                    { "message": "There was an error saving the images."}
            }, status=500)