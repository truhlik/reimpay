from .base import *


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'reimpay',
        'USER': 'reimpay',
        'PASSWORD': 'reimpay',
        'HOST': 'postgres',
        'PORT': 5432,
    }
}
SECRET_KEY = 'testing'
SMARTFORM_API_KEY = 'test'
