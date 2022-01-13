import contextlib
from urllib.request import Request, urlopen
from datetime import timedelta
from urllib3 import ProxyManager

from django.conf import settings
from minio import Minio

IS_LOCALHOST = 'localhost' in settings.MINIO_ENDPOINT.find('localhost')

MINIO_PROXY = 'https://' if settings.MINIO_USE_SSL else 'http://' \
    + settings.MINIO_ENDPOINT + '/'

if IS_LOCALHOST:
    MINIO_PROXY = MINIO_PROXY.replace(
        '://localhost', '://host.docker.internal'
    )

MINIO = Minio(
    settings.MINIO_ENDPOINT,
    access_key=settings.MINIO_ACCESS_KEY,
    secret_key=settings.MINIO_SECRET_KEY,
    secure=settings.MINIO_USE_SSL,
    http_client=ProxyManager(MINIO_PROXY),
)


def minio_get_object(object_name):
    return MINIO.presigned_get_object(
        bucket_name=settings.MINIO_BUCKET_NAME,
        object_name=object_name,
        expires=timedelta(seconds=3600)
    )


def minio_put_object(object_name):
    return MINIO.presigned_put_object(
        bucket_name=settings.MINIO_BUCKET_NAME,
        object_name=object_name,
        expires=timedelta(seconds=7200)
    )


def minio_remove_object(object_name):
    return MINIO.remove_object(
        bucket_name=settings.MINIO_BUCKET_NAME,
        object_name=object_name
    )


def url_retrieve(filename):
    """
    This function retrieves the object from minio and streams it to a local
    file.
    This serves as a work-around for local development using docker.
    minio:9000 or host.docker.internal:9000 are both inaccessible via browser
    which means our front-end wouldn't be able to access it. 
    The alternative solution is to modify the system's hosts file. But that
    requires some manual process.
    Copied from:
    https://github.com/python/cpython/blob/23c5f93b83f78f295313e137011edb18b24c37c2/Lib/urllib/request.py#L221-L282
    """
    url = minio_get_object(filename)

    if IS_LOCALHOST:
        url = url.replace('://localhost', '://host.docker.internal')

    req = Request(url, headers={
        'HOST': settings.MINIO_ENDPOINT
    })

    try:
        with contextlib.closing(urlopen(req)) as file_path:
            temp_file_path = open(filename, 'wb')

            with temp_file_path:
                byte_size = 1024 * 8

                while True:
                    block = file_path.read(byte_size)
                    if not block:
                        break
                    temp_file_path.write(block)
    except Exception as error:
        print(error)

    return True
