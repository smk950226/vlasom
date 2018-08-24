from .common import *
import os
import pymysql

pymysql.install_as_MySQLdb()

DATABASES = {
    'default': {
        'ENGINE': os.environ.get('DB_ENGINE', 'django.db.backends.mysql'),
        'HOST': get_secret("DB_HOST"),
        'USER': get_secret("DB_USER"),
        'PASSWORD': get_secret("DB_PASSWORD"),
        'NAME': get_secret("DB_NAME"),
        'PORT': get_secret("DB_PORT"),
    },
}

INSTALLED_APPS += ['storages',]

STATICFILES_STORAGE = 'vlasom.storages.StaticS3Boto3Storage'
DEFAULT_FILE_STORAGE = 'vlasom.storages.MediaS3Boto3Storage'

AWS_ACCESS_KEY_ID = get_secret("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = get_secret("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = get_secret("AWS_STORAGE_BUCKET_NAME")
AWS_S3_REGION_NAME = get_secret("AWS_S3_REGION_NAME")

SITE_ID = 2

DEBUG = False

ALLOWED_HOSTS = ['www.vlasom.com', '127.0.0.1']

ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'https'

AWS_QUERYSTRING_AUTH = False