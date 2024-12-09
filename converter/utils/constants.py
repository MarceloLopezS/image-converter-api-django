# Pillow format docs:
# https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html
ICO = "ico"
JPG = "jpg"
JPEG = "jpeg"
PNG = "png"
WEBP = "webp"
MAX_FILE_SIZE_BYTES = 10 * 1024 * 1024
ALLOWED_IO = {
  "input": {
    "file_extensions": [ ICO, JPG, JPEG, PNG, WEBP ],
    "max_file_size_bytes": MAX_FILE_SIZE_BYTES
  },
  "output": {
    "file_formats": [ ICO, JPEG, PNG, WEBP ]
  }
}
DEFAULT_QUALITY = 95
FORMAT_PARAMS = {
  ICO: [
    {
      "name": "sizes",
      "label": "Sizes",
      "description": "List of valid ICO sizes, in pixels.",
      "options": [
        [16, 16],
        [32, 32],
        [64, 64],
        [128, 128],
        [256, 256],
      ],
      "default": [128, 128]
    }
  ],
  JPEG: [
    {
      "name": "quality",
      "label": "Image quality",
      "description": "From 0 to 100. Higher is better, but larger size.",
      "is_range": 1,
      "min": 0,
      "max": 100,
      "default": DEFAULT_QUALITY
    },
    {
      "name": "optimize",
      "label": "Encoder optimization",
      "description": \
        "Optimize encoder settings. Improves quality at the cost of speed.",
      "is_bool": 1,
      "default": 0
    },
    {
      "name": "progressive",
      "label": "Progressive JPEG",
      "description": "Output a progressive JPEG file.",
      "is_bool": 1,
      "default": 0
    },
    {
      "name": "exif",
      "label": "Keep metadata",
      "description": \
        "Keep color profiles, EXIF and comments. This may increase file size.",
      "is_bool": 1,
      "default": 0
    }
  ],
  PNG: [
    {
      "name": "compress_level",
      "label": "Compression level",
      "description": \
        "From 0 to 9. Lower is faster convertion speed, but larger file size.",
      "is_range": 1,
      "min": 0,
      "max": 9,
      "default": 6
    },
    {
      "name": "exif",
      "label": "Keep metadata",
      "description": \
        "Keep color profiles, EXIF and comments. This may increase file size.",
      "is_bool": 1,
      "default": 0
    }
  ],
  WEBP: [
    {
      "name": "lossless",
      "label": "Lossless compression",
      "description": \
        "Compress without any quality loss. Can impact file size negatively.",
      "is_bool": 1,
      "default": 0,
      "disables_params_on_value" : {
        0: [],
        1: [ "quality", "method" ]
      }
    },
    {
      "name": "quality",
      "label": "Image quality",
      "description": "From 0 to 100. Higher is better, but larger size.",
      "is_range": 1,
      "min": 0,
      "max": 100,
      "default": DEFAULT_QUALITY
    },
    {
      "name": "method",
      "label": "Processing effort",
      "description": \
        "Quality/speed tradeoff from 0 to 6. Higher is better quality, but slower.",
      "is_range": 1,
      "min": 0,
      "max": 6,
      "default": 4
    },
    {
      "name": "exif",
      "label": "Keep metadata",
      "description": \
        "Keep color profiles, EXIF and comments. This may increase file size.",
      "is_bool": 1,
      "default": 0
    }
  ]
}