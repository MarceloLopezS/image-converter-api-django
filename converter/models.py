from functools import cmp_to_key

from django.db import models
from django.forms.models import model_to_dict

# Create your models here.

class InputFileExtension(models.Model):
    id = models.SmallAutoField(primary_key=True)
    name = models.CharField(max_length=5)

    def __str__(self):
        return f"{self.name}"


class OutputParamRangeField(models.Model):
    id = models.SmallAutoField(primary_key=True)
    name = models.CharField(max_length=30, unique=True)
    label = models.CharField(max_length=60, unique=True)
    description = models.CharField(max_length=100)
    is_range = \
      models.BooleanField(auto_created=True, default=True, editable=False)
    min = models.SmallIntegerField()
    max = models.SmallIntegerField()
    default = models.SmallIntegerField()

    def __str__(self):
        return f"{self.label} | Default value: {self.default}"


class OutputParamSelectField(models.Model):
    id = models.SmallAutoField(primary_key=True)
    name = models.CharField(max_length=30, unique=True)
    label = models.CharField(max_length=60, unique=True)
    description = models.CharField(max_length=100)
    options = models.JSONField()
    default = models.JSONField()
    
    def __str__(self):
        return f"{self.label} | Default value: {self.default}"


class OutputParamBoolField(models.Model):
    id = models.SmallAutoField(primary_key=True)
    name = models.CharField(max_length=30, unique=True)
    label = models.CharField(max_length=60, unique=True)
    description = models.CharField(max_length=100)
    is_bool = \
      models.BooleanField(auto_created=True, default=True, editable=False)
    default = models.BooleanField()
    disabled_range_fields_on_enabled = models.ManyToManyField(
        OutputParamRangeField,
        related_name="disabled_range_field_in_enabled_bool_fields",
        blank=True
    )
    disabled_select_fields_on_enabled = models.ManyToManyField(
        OutputParamSelectField,
        related_name="disabled_select_field_in_enabled_bool_fields",
        blank=True
    )

    def __str__(self):
        return f"{self.label} | Default value: {self.default}"
    

class OutputFormat(models.Model):
    id = models.SmallAutoField(primary_key=True)
    name = models.CharField(max_length=10, unique=True)
    output_param_bool_fields = models.ManyToManyField(
        OutputParamBoolField,
        related_name="bool_field_in_output_formats",
        blank=True
    )
    output_param_range_fields = models.ManyToManyField(
        OutputParamRangeField,
        related_name="range_field_in_output_formats",
        blank=True
    )
    output_param_select_fields = models.ManyToManyField(
        OutputParamSelectField,
        related_name="select_field_in_output_formats",
        blank=True
    )

    def get_output_param_fields(self):
        fields = []
        bool_fields = []
        range_fields = []
        select_fields = []

        try:
            bool_fields_query_set = self.output_param_bool_fields.all()

            bool_fields = list()

            for bool_field in bool_fields_query_set:
                formatted_bool_field = {
                    k:v for (k, v) in model_to_dict(bool_field).items()
                }
                del formatted_bool_field["id"]
                del formatted_bool_field["disabled_range_fields_on_enabled"]
                del formatted_bool_field["disabled_select_fields_on_enabled"]

                formatted_bool_field["is_bool"] = bool_field.is_bool
                formatted_bool_field["disabled_fields_on_enabled"] = \
                  list(
                      bool_field.disabled_range_fields_on_enabled\
                      .values_list("name", flat=True)
                  ) + list(
                      bool_field.disabled_select_fields_on_enabled\
                      .values_list("name", flat=True)
                  )
                
                if len(
                    formatted_bool_field["disabled_fields_on_enabled"]
                ) == 0:
                    del formatted_bool_field["disabled_fields_on_enabled"]
                
                bool_fields.append(formatted_bool_field)
        except:
            pass
        try:
            range_fields = list(self.output_param_range_fields.values(
                "name", "label", "description",
                "is_range", "min", "max", "default"
            ))
        except:
            pass
        try:
            select_fields = list(self.output_param_select_fields.values(
                "name", "label", "description", "options", "default"
            ))
        except:
            pass
        
        fields = bool_fields + range_fields + select_fields
        return fields

    def __str__(self):
        return f"{self.name}"


class UnsupportedTransparencyFormat(models.Model):
    id = models.SmallAutoField(primary_key=True)
    output_format = models.OneToOneField(
        OutputFormat,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.output_format}"


class ImageConverter:
    def __init__(self, image_processor):
        self.__processor = image_processor

    def convert(self, input_image, output_image_path, output_format, **kwargs):
        """
        Converts an image to the specified format.
        Raises an exception if an error ocurrs.
        Returns the image path of the converted output.
        """
        if not isinstance(output_image_path, str):
            raise Exception("Output image path must be a string.")

        try:
            mod_args = {}
            for arg in kwargs:
                mod_args[arg] = kwargs[arg]

            with self.__processor.open(input_image) as image:
                unsupported_transparency_format_objects = \
                  UnsupportedTransparencyFormat.objects.all()
                
                unsupported_transparency_formats = list(map(
                    lambda format_obj: format_obj.output_format.name,
                    unsupported_transparency_format_objects
                ))
                
                if output_format in unsupported_transparency_formats:
                    image = image.convert("RGB")
                    mod_args["keep_rgb"] = True

                if mod_args.get("exif") == True:
                    mod_args["exif"] = image.getexif()
                    
                image.save(
                    output_image_path,
                    output_format,
                    **mod_args
                )
        except Exception as err:
            raise Exception(f"Convertion processor error: {err}")
        
        return output_image_path