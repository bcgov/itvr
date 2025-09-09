from minio import Minio
from django.conf import settings


def get_minio_client():
    return Minio(
        settings.MINIO_ENDPOINT,
        settings.MINIO_ACCESS_KEY,
        settings.MINIO_SECRET_KEY,
        secure=(settings.MINIO_USE_SSL == "True"),
    )


def get_minio_object(object_name):
    client = get_minio_client()
    return client.get_object(settings.MINIO_BUCKET_NAME, object_name)
