from .base import *
from config.env import env

env.read_env(BASE_DIR / '.env.production')
DEBUG = False

ALLOWED_HOSTS = env('ALLOWED_HOSTS')

DATABASES = {
    'default': {
        'ENGINE': env('DB_ENGINE'),
        'NAME': env('DB_NAME'),
    }
}
