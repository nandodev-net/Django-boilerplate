import os
from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = origins.split(" ") if (origins := os.getenv("DJANGO_ALLOWED_HOSTS", default="")) else []
CSRF_TRUSTED_ORIGINS = origins.split(" ") if (origins := os.getenv("CSRF_TRUSTED_ORIGINS", default="")) else []
