class AllowedIOController:
    def __init__(self, handle_get_allowed_IO):
      self.__get_allowed_IO = handle_get_allowed_IO
    
    def get_io_params(self, max_file_size_bytes, json_response):
        return json_response(
              self.__get_allowed_IO(max_file_size_bytes),
              status=200
        )
    
class OutputParamFieldsController:
    def __init__(self, handle_get_output_format_param_fields):
        self.__get_output_format_param_fields = \
          handle_get_output_format_param_fields

    def get_related_to_format(self, request, json_response):
        output_format = request.POST.get("output_format")

        if not output_format or len(output_format) == 0:
            return json_response({
                "status": "fail",
                "data": { "message": "No output format specified." }
            }, status=400)
        
        try:
            params = self.__get_output_format_param_fields(output_format)
            return json_response({
                "status": "success",
                "data": {
                    "output_params": params
                }
            }, status=200)
        except Exception as err:
            print(f"Invalid format name: {err}")
            return json_response({
                "status": "fail",
                "data": {
                    "message": "Invalid format name."
                }
            }, status=400)