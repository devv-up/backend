import json

from .base import *

with open(os.path.join(BASE_DIR, 'secrets.json')) as file:
    SECRETES = json.loads(file.read())

SECRET_KEY = SECRETES['SECRET_KEY']

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': SECRETES['POSTGRESQL_HOST'],
        'NAME': SECRETES['POSTGRESQL_NAME'],
        'USER': SECRETES['POSTGRESQL_USER'],
        'PASSWORD': SECRETES['POSTGRESQL_PASSWORD'],
        'PORT': SECRETES['POSTGRESQL_PORT'],
    }
}
