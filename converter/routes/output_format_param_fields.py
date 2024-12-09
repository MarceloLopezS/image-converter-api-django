from ..models import OutputFormat
from ..usecases.get_output_format_param_fields import \
  get_output_format_param_fields
from ..controllers.io_params import OutputParamFieldsController

output_format_model = OutputFormat
handle_get_output_format_param_fields = \
  get_output_format_param_fields(output_format_model)

output_param_fields_controller = \
  OutputParamFieldsController(handle_get_output_format_param_fields)