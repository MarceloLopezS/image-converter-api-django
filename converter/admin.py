from django.contrib import admin

from .models import InputFileExtension, OutputParamBoolField, \
  OutputParamRangeField, OutputParamSelectField, OutputFormat, \
  UnsupportedTransparencyFormat

# Register your models here.

admin.site.register(InputFileExtension)
admin.site.register(OutputParamRangeField)
admin.site.register(OutputParamSelectField)
admin.site.register(OutputParamBoolField)
admin.site.register(OutputFormat)
admin.site.register(UnsupportedTransparencyFormat)