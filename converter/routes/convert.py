from PIL import Image

from ..models import ImageConverter
from ..usecases.convert_image import convert_image

from ..models import InputFileExtension, OutputFormat
from ..usecases.get_allowed_input_file_extensions import \
  get_allowed_input_file_extensions
from ..usecases.get_allowed_output_formats import \
  get_allowed_output_formats
from ..usecases.get_allowed_output_params import \
  get_allowed_output_params
from ..usecases.get_formatted_output_params import \
  get_formatted_output_params

from ..controllers.image import ImageConvertController

image_model = ImageConverter(Image)
handle_image_convert = convert_image(image_model)

allowed_input_file_extensions_model = InputFileExtension
handle_get_allowed_input_file_extensions = \
  get_allowed_input_file_extensions(allowed_input_file_extensions_model)

allowed_output_formats_model = OutputFormat
handle_get_allowed_output_formats = \
  get_allowed_output_formats(allowed_output_formats_model)

allowed_output_params_model = OutputFormat
handle_get_allowed_output_params = \
  get_allowed_output_params(allowed_output_params_model)

format_output_params_model = OutputFormat
handle_get_formatted_output_params = \
  get_formatted_output_params(format_output_params_model)

image_controller = ImageConvertController(
  handle_image_convert,
  handle_get_allowed_input_file_extensions,
  handle_get_allowed_output_formats,
  handle_get_allowed_output_params,
  handle_get_formatted_output_params
)