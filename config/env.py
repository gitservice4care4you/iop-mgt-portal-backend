from pathlib import Path
import environ
import os

# Initialize environ
env = environ.Env(
    DEBUG=(bool, False),
    ALLOWED_HOSTS=(list, ["*"]),
    DB_PORT=(int, 5432)
)

BASE_DIR = Path(__file__).resolve().parent.parent


