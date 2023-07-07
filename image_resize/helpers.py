import hashlib
import os

from django.conf import settings
from django.core.files.storage import default_storage
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
from .utils import upload_image


def resize_image(file_name: str, image_file: InMemoryUploadedFile, width: int, height: int) -> str:
    image = Image.open(image_file)

    if not height:
        ratio = width / image.width
        height = int(image.height * ratio)
    new_image = image.resize((width, height))

    image_name = generate_image_name(file_name, width, height, image.format)
    if not default_storage.exists(image_name):
        new_image_path = os.path.join(settings.MEDIA_ROOT, image_name)
        new_image.save(new_image_path, image.format)
        upload_image(new_image_path)
    return image_name


def generate_image_name(name: str, width: int, height: int, image_format: str) -> str:
    return f"{hashlib.md5(name.encode('utf-8')).hexdigest()}_{width}x{height}.{image_format}"
