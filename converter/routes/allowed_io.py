from ..models import InputFileExtension, OutputFormat
from ..usecases.get_allowed_io import get_allowed_io
from ..controllers.io_params import AllowedIOController

input_file_extension_model = InputFileExtension
output_format_model = OutputFormat
handle_get_allowed_io = \
  get_allowed_io(input_file_extension_model, output_format_model)

allowed_IO_controller = \
  AllowedIOController(handle_get_allowed_io)