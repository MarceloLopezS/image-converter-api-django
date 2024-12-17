import os
from io import BytesIO
import zipfile

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
            
        
class DownloadAllFilesController:
    def __init__(
      self,
      handle_get_converted_file_name,
      handle_get_file_relative_location
    ):
        self.__get_file_relative_location = handle_get_file_relative_location
        self.__get_converted_file_name = handle_get_converted_file_name

    
    def download(
      self,
      request,
      media_root,
      file_constructor,
      json_response,
      file_response
    ):
        file_uuids = request.POST.getlist("convertion_id")
        file_uuids = list(filter(
            lambda uuid: isinstance(uuid, str) and len(uuid) > 0, file_uuids
        ))

        if len(file_uuids) == 0:
            return json_response({
                "status": "fail",
                "data": { "message": "Missing convertion ids." }
            }, status=400)
        
        try:
            output_files = list(map(
                lambda file_uuid: {
                    "name": self.__get_converted_file_name(file_uuid),
                    "location": os.path.join(
                        media_root,
                        self.__get_file_relative_location(file_uuid)
                    )
                },
                file_uuids
            ))
            
            buffer = BytesIO()

            with zipfile.ZipFile(buffer, "a", zipfile.ZIP_DEFLATED, False) \
              as zip_file:
                for output_file in output_files:
                    with open(output_file["location"], "rb") as file:
                        zip_file.writestr(output_file["name"], file.read())

            buffer.seek(0)

            return file_response(
                file_constructor(buffer),
                as_attachment=True,
                status=200
            )
                
        except Exception as err:
            print(err)
            return json_response({
                "status": "fail",
                "data": {
                    "message": "An error ocurred during files retrieve."
                }
            }, status=500)