import os
import sys
from pathlib import Path
from . import email
from . import messages_custom

AUTH_USER_MODEL = "users.ITVRUser"

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv(
    "DJANGO_SECRET_KEY", "#8+m(ba_(ra1=lo+-7jyp#x49l27guk*i4)w@xp7j9b9umkwh^"
)

SALT_KEY = os.getenv("DJANGO_SALT_KEY", "0123456789abcdefghijklmnopqrstuvwxyz")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("DJANGO_DEBUG", "False") == "True"
TESTING = "test" in sys.argv

CORS_ORIGIN_WHITELIST = [os.getenv("CORS_ORIGIN_WHITELIST", "http://localhost:3000")]

ALLOWED_HOSTS = [os.getenv("ALLOWED_HOSTS", "*")]

CSRF_TRUSTED_ORIGINS = [
    os.getenv("CORS_ORIGIN_WHITELIST", "http://localhost:3000"),
    os.getenv("BACKEND_ORIGIN", "http://localhost:8000"),
]

# Application definition
INSTALLED_APPS = [
    "jazzmin",
    "api.apps.ITVRAdminConfig",
    "django_filters",
    "django_extensions",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.messages",
    "django.contrib.sessions",
    "django.contrib.staticfiles",
    "rest_framework",
    "corsheaders",
    "django_q",
    "sequences.apps.SequencesConfig",
    "users",
    "api.apps.ApiConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "api.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    }
]

WSGI_APPLICATION = "api.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": os.getenv("DB_ENGINE", "django.db.backends.postgresql"),
        "NAME": os.getenv("DB_NAME", "postgres"),
        "USER": os.getenv("DB_USER", "postgres"),
        "PASSWORD": os.getenv("DB_PASSWORD", "postgres"),
        "HOST": os.getenv("DB_HOST", "db"),
        "PORT": os.getenv("DB_PORT", "5432"),
    },
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators
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
# https://docs.djangoproject.com/en/3.1/topics/i18n/
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Canada/Pacific"
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/
PUBLIC_DIR = os.path.join(BASE_DIR, "public")
STATICFILES_DIRS = [PUBLIC_DIR]
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATIC_URL = "/static/"


BYPASS_AUTHENTICATION = os.getenv("BYPASS_AUTHENTICATION", "False") == "True"

AUTHENTICATION_CLASSES = [
    "api.authentication.keycloak.KeycloakAuthentication",
    "rest_framework.authentication.SessionAuthentication",
    "rest_framework.authentication.BasicAuthentication",
]

if BYPASS_AUTHENTICATION:
    AUTHENTICATION_CLASSES = ["api.authentication.testing.LoadTestingAuthentication"]

# Django Rest Framework Settings
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": AUTHENTICATION_CLASSES,
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "COERCE_DECIMAL_TO_STRING": False,
    "DEFAULT_PAGINATION_CLASS": "api.pagination.StandardResultsSetPagination",
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
        "api.filters.order_by.RelatedOrderingFilter",
    ],
}


BCEID_KEYCLOAK_CLIENT_ID = os.getenv("BCEID_KEYCLOAK_CLIENT_ID")
BCEID_KEYCLOAK_REALM = os.getenv("BCEID_KEYCLOAK_REALM")
BCEID_KEYCLOAK_URL = os.getenv("BCEID_KEYCLOAK_URL")

BCSC_KEYCLOAK_CLIENT_ID = os.getenv("BCSC_KEYCLOAK_CLIENT_ID")
BCSC_KEYCLOAK_REALM = os.getenv("BCSC_KEYCLOAK_REALM")
BCSC_KEYCLOAK_URL = os.getenv("BCSC_KEYCLOAK_URL")


MINIO_ACCESS_KEY = os.getenv("MINIO_ROOT_USER")
MINIO_SECRET_KEY = os.getenv("MINIO_ROOT_PASSWORD")
MINIO_BUCKET_NAME = os.getenv("MINIO_BUCKET_NAME")
MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT")

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"


# S3 configuration (for media)

DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

AWS_ACCESS_KEY_ID = MINIO_ACCESS_KEY
AWS_SECRET_ACCESS_KEY = MINIO_SECRET_KEY
AWS_STORAGE_BUCKET_NAME = MINIO_BUCKET_NAME
AWS_S3_ENDPOINT_URL = MINIO_ENDPOINT
AWS_DEFAULT_ACL = None
AWS_QUERYSTRING_AUTH = True
AWS_S3_FILE_OVERWRITE = False

# Email configuration

EMAIL = email.config()


Q_CLUSTER = {
    "name": "ITVR",
    "workers": 4,
    "timeout": 90,
    "retry": 1260,
    "queue_limit": 50,
    "bulk": 10,
    "orm": "default",
    "save_limit": 20 if DEBUG else -1,
    "max_attempts": 100,
}

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.db.DatabaseCache",
        "LOCATION": "itvr_cache_table",
    }
}

JAZZMIN_SETTINGS = {
    # title of the window (Will default to current_admin_site.site_title if absent or None)
    "site_title": "BC Gov ITVR",
    # Title on the login screen (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    "site_header": "BC Gov ITVR",
    # Title on the brand (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    "site_brand": "BC Gov ITVR",
}

CRA_ENVIRONMENT = os.getenv("CRA_ENVIRONMENT", "A")

# NCDA Sharepoint config
NCDA_CLIENT_ID = os.getenv(
    "NCDA_CLIENT_ID",
    "d4d97d40-bb26-44f8-ba70-c677471d6cc1@1d4864aa-f2da-42dc-a62a-34b4dd790b6a",
)
NCDA_CLIENT_SECRET = os.getenv("NCDA_CLIENT_SECRET")
NCDA_RESOURCE = os.getenv(
    "NCDA_RESOURCE",
    "00000003-0000-0ff1-ce00-000000000000/newcardealers.sharepoint.com@1d4864aa-f2da-42dc-a62a-34b4dd790b6a",
)
NCDA_AUTH_URL = os.getenv(
    "NCDA_AUTH_URL",
    "https://accounts.accesscontrol.windows.net/1d4864aa-f2da-42dc-a62a-34b4dd790b6a/tokens/OAuth/2/",
)
NCDA_SHAREPOINT_URL = os.getenv(
    "NCDA_SHAREPOINT_URL",
    "https://newcardealers.sharepoint.com/sites/ElectricVehicleRebateApplications/_api/web",
)

MESSAGE_TAGS = messages_custom.TAGS

RUN_JOBS = os.getenv("RUN_JOBS", False)

VIRUS_SCANNING_ENABLED = os.getenv("VIRUS_SCANNING_ENABLED", False)
CLAMD_HOST = os.getenv("CLAMD_HOST", "clamav")
CLAMD_PORT = int(os.getenv("CLAMD_PORT", 3310))
