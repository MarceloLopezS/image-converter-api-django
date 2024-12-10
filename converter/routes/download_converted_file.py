from ..models import ConvertedFile
from ..usecases.get_converted_file_relative_location import \
  get_converted_file_relative_location
from ..controllers.download import DownloadFileController

converted_file_model = ConvertedFile
handle_get_converted_file_relative_location = \
  get_converted_file_relative_location(converted_file_model)

download_file_controller = DownloadFileController(
    handle_get_converted_file_relative_location
)