from .base import *
from config.env import env
import os

env.read_env(os.path.join(BASE_DIR, ".env"))

DEBUG = True
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["*"])

# Direct PostgreSQL configuration without env variables
DATABASES = {
    "default": {
        "ENGINE": env("DB_ENGINE"),
        "NAME": env("DB_NAME"),
        "USER": env("DB_USER"),
        "PASSWORD": env("DB_PASSWORD"),
        "HOST": env("DB_HOST"),
        "PORT": env("DB_PORT"),
    }
}
