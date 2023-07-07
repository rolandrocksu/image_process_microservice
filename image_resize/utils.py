from minio import Minio
from pathlib import Path
import logging
from django.conf import settings


def upload_image(path: str):
    client = Minio(
        "minio:9000",
        access_key=settings.MINIO_ACCESS_KEY,
        secret_key=settings.MINIO_PASSWORD,
        secure=False,
    )
    """Uploads image to the images bucket"""
    # Make 'image' bucket if not exist.
    found = client.bucket_exists(settings.MINIO_BUCKET_NAME)
    if not found:
        client.make_bucket(settings.MINIO_BUCKET_NAME)
        logging.info(f"Created '{settings.MINIO_BUCKET_NAME}' bucket")

    value = client.fput_object(
        settings.MINIO_BUCKET_NAME, Path(path).name, path, content_type="image/png",
    )
    print("#" * 100, value)
