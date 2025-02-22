from django.conf import settings
from django.core.files import File
from django.http import FileResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .utils.constants import MAX_FILE_SIZE_BYTES

from .controllers.decorators.rate_limit import rate_limit

from .routes.allowed_io import allowed_IO_controller
from .routes.output_format_param_fields import output_param_fields_controller
from .routes.convert import image_controller
from .routes.download_converted_file import download_file_controller
from .routes.download_all_converted_files import download_all_files_controller

# Create your views here.

def index(request):
    if request.method == "GET":
        return JsonResponse({ "status": "success" }, status=200)
  

def allowed_io_params(request):
    if request.method == "GET":
        return allowed_IO_controller.get_io_params(
            MAX_FILE_SIZE_BYTES,
            JsonResponse
        )
  
  
@csrf_exempt
def output_format_param_fields(request):
   if request.method == "POST":
        return output_param_fields_controller.get_related_to_format(
            request,
            JsonResponse
        )
   

@csrf_exempt
@rate_limit(key='ip', rate='20/d')
def convert(request):
    if request.method == "POST":
        return image_controller.convert(
            request,
            JsonResponse
        )
    

@csrf_exempt
@rate_limit(key='ip', rate='20/d')
def download_converted_file(request):
    if request.method == "POST":
        return download_file_controller.download_file(
            request,
            settings.MEDIA_ROOT,
            JsonResponse,
            FileResponse
        )
    

@csrf_exempt
def dowload_all_converted_files(request):
    if request.method == "POST":
        return download_all_files_controller.download(
            request,
            settings.MEDIA_ROOT,
            File,
            JsonResponse,
            FileResponse
        )