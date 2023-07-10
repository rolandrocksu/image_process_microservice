import json
import logging
from pathlib import Path

from django.conf import settings
from minio import Minio
from minio.commonconfig import ENABLED


class MinioClient:

    def __init__(self, access_key: str, secret_key: str):
        self.client = Minio(
            "minio:9000",
            access_key=access_key,  # settings.MINIO_ACCESS_KEY,
            secret_key=secret_key,  # settings.MINIO_PASSWORD,
            secure=False,
        )

    def upload_object(self, path: str) -> None:

        """Uploads image to the images bucket"""
        # Make 'image' bucket if not exist.
        found = self.client.bucket_exists(settings.MINIO_BUCKET_NAME)
        if not found:
            # TODO
            self.create_public_read_only_bucket(settings.MINIO_BUCKET_NAME)

        self.client.fput_object(
            settings.MINIO_BUCKET_NAME, Path(path).name, path, content_type="image/png",
        )

    def create_public_read_only_bucket(self, bucket_name: str) -> None:
        self.client.make_bucket(bucket_name)
        logging.info(f"Created '{bucket_name}' bucket")

        # Set bucket policy to make it public
        policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {"AWS": "*"},
                    "Action": ["s3:GetBucketLocation", "s3:ListBucket"],
                    "Resource": "arn:aws:s3:::my-bucket",
                },
                {
                    "Effect": "Allow",
                    "Principal": {"AWS": "*"},
                    "Action": "s3:GetObject",
                    "Resource": "arn:aws:s3:::my-bucket/*",
                },
            ],
        }
        self.client.set_bucket_policy("my-bucket", json.dumps(policy))
        logging.info(f"Set '{settings.MINIO_BUCKET_NAME}' bucket policy to public")
