from django.urls import path

from . import views

urlpatterns = [
  path("", views.index, name="index"),
  path(
    "allowed-io-params",
    views.allowed_io_params,
    name="allowed_io_params"
  ),
  path(
    "output-format-param-fields",
    views.output_format_param_fields,
    name="index"
  ),
  path("convert", views.convert, name="convert"),
  path(
    "download-converted-file",
    views.download_converted_file,
    name="download_converted_file"
  ),
  path(
    "download-all-converted-files",
    views.dowload_all_converted_files,
    name="download_all_converted_files"
  )
]