import os
from pathlib import Path

# ------------------------------
# Base Paths
# ------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# ------------------------------
# SECURITY
# ------------------------------
SECRET_KEY = 'django-insecure-w6_g!$#eajvl7ey-d=u1@9lg4h#=1a0jpudk1i&26n2jem0+9c'
DEBUG = True
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '10.1.1.63']

# ------------------------------
# Installed Apps
# ------------------------------
INSTALLED_APPS = [
    # Django default apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'django_extensions',
    # Your apps
    "humans",
    "profiles",
    "posts",
]

# ------------------------------
# Middleware
# ------------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# ------------------------------
# URL Config
# ------------------------------
ROOT_URLCONF = "rekjrc.urls"

# ------------------------------
# Templates
# ------------------------------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],  # Put your HTML templates here
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# ------------------------------
# WSGI
# ------------------------------
WSGI_APPLICATION = "rekjrc.wsgi.application"

# ------------------------------
# Database
# ------------------------------
DATABASES = {
    'default': {
        'ENGINE': 'mssql',
        'NAME': 'RekjRC_django',
        'USER': 'rekjrc_django',
        'PASSWORD': 'TtQJBQKFy5vydN35Fh3zYdmv',
        'HOST': 'localhost,1433',
        'OPTIONS': {
            'driver': 'ODBC Driver 17 for SQL Server',
            'Encrypt': 'yes',
            'TrustServerCertificate': 'yes',
        },
    }
}

# ------------------------------
# Password Validation
# ------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# ------------------------------
# Internationalization
# ------------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# ------------------------------
# Static & Media files
# ------------------------------
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# ------------------------------
# Default Primary Key Type
# ------------------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ------------------------------
# Custom User Model
# ------------------------------
AUTH_USER_MODEL = "humans.Human"

# settings.py
LOGIN_REDIRECT_URL = '/'  # redirect to homepage after login
LOGOUT_REDIRECT_URL = '/'  # optional: redirect to homepage after logout
