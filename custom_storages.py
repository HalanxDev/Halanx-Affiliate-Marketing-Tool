from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage

from utility.environments import DEVELOPMENT


# noinspection PyAbstractClass
class StaticStorage(S3Boto3Storage):
    if settings.ENVIRONMENT != DEVELOPMENT:
        location = settings.AWS_STATIC_LOCATION


# noinspection PyAbstractClass
class PublicMediaStorage(S3Boto3Storage):
    if settings.ENVIRONMENT != DEVELOPMENT:
        location = settings.AWS_PUBLIC_MEDIA_LOCATION
        file_overwrite = False


# noinspection PyAbstractClass
class PrivateMediaStorage(S3Boto3Storage):
    if settings.ENVIRONMENT != DEVELOPMENT:
        location = settings.AWS_PRIVATE_MEDIA_LOCATION
        default_acl = 'private'
        file_overwrite = False
        custom_domain = False
