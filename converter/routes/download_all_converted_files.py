from ..models import ConvertedFile
from ..usecases.get_converted_file_name import \
  get_converted_file_name
from ..usecases.get_converted_file_relative_location import \
  get_converted_file_relative_location
from ..controllers.download import DownloadAllFilesController

converted_file_model = ConvertedFile
handle_get_converted_file_name = \
  get_converted_file_name(converted_file_model)
handle_get_converted_file_relative_location = \
  get_converted_file_relative_location(converted_file_model)

download_all_files_controller = DownloadAllFilesController(
    handle_get_converted_file_name,
    handle_get_converted_file_relative_location
)