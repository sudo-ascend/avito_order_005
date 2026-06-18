"""
Django settings for config project.
"""

import ast
import os
from pathlib import Path
from urllib.parse import urlsplit

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent


def env_bool(name, default=False):
    value = os.environ.get(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def env_list(name, default):
    value = os.environ.get(name)
    if not value:
        return default
    try:
        parsed = ast.literal_eval(value)
    except (SyntaxError, ValueError):
        parsed = None
    if isinstance(parsed, (list, tuple, set)):
        return [str(item).strip() for item in parsed if str(item).strip()]
    return [item.strip() for item in value.split(",") if item.strip()]


# Загружаем .env файл
env_path = BASE_DIR / '.env'
if env_path.exists():
    load_dotenv(env_path, override=True)


DEBUG = env_bool("DEBUG", False)


# ====== БЕЗОПАСНОСТЬ ======
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "dev-secret-key-12345")
SITE_URL = os.environ.get("SITE_URL", "https://aquaklon.ru").rstrip("/")
if not SITE_URL.startswith(("http://", "https://")):
    SITE_URL = f"https://{SITE_URL}"
SITE_HOST = urlsplit(SITE_URL).netloc
SEO_NOINDEX = env_bool("SEO_NOINDEX", False)

# =========================


default_allowed_hosts = [SITE_HOST]
if SITE_HOST.startswith("www."):
    default_allowed_hosts.append(SITE_HOST.removeprefix("www."))
else:
    default_allowed_hosts.append(f"www.{SITE_HOST}")
default_allowed_hosts.extend(["127.0.0.1", "localhost"])

ALLOWED_HOSTS = env_list("ALLOWED_HOSTS", default_allowed_hosts)


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "catalog",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


ROOT_URLCONF = "config.urls"


# ====== СТАТИЧЕСКИЕ ФАЙЛЫ ======
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_DIRS = [
    BASE_DIR / "static",
] if (BASE_DIR / "static").exists() else []

# ====== МЕДИА ФАЙЛЫ ======
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"


# ====== ШАБЛОНЫ ======
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "templates",
        ] if (BASE_DIR / "templates").exists() else [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
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


# Internationalization
LANGUAGE_CODE = "ru"
TIME_ZONE = "Europe/Moscow"
USE_I18N = True
USE_TZ = True


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGIN_URL = "/admin/login/"
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")


# Хранилище для статики
staticfiles_backend = "django.contrib.staticfiles.storage.StaticFilesStorage"
if not DEBUG:
    staticfiles_backend = "whitenoise.storage.CompressedManifestStaticFilesStorage"

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": staticfiles_backend,
    },
}

WHITENOISE_MAX_AGE = 0 if DEBUG else 31536000
