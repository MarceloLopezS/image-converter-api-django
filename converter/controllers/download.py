import os

class DownloadFileController:
    def __init__(self, handle_get_file_relative_location):
        self.__get_file_relative_location = handle_get_file_relative_location

    def download_file(self, request, media_root, json_response, file_response):
        file_uuid = request.POST.get("convertion_id")

        if not file_uuid or len(file_uuid) == 0:
            return json_response({
                "status": "fail",
                "data": { "message": "Missing convertion id." }
            }, status=400)
        
        try:
            file_relative_location = \
              self.__get_file_relative_location(file_uuid)
            file_location = os.path.join(media_root, file_relative_location)

            return file_response(
              open(file_location, "rb"),
              as_attachment=True,
              status=200
            )
        except:
            return json_response({
                "status": "fail",
                "data": { "message": "An error ocurred during file retrieve." }
            }, status=500)