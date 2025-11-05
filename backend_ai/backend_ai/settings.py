from pathlib import Path
import environ
import os
from corsheaders.defaults import default_headers, default_methods


env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False),
    SECRET_KEY=(str, "secret_key"),
)


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Take environment variables from .env file
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["localhost", "backend-ai"])

FRONTEND_URL = "http://localhost:5173"

# OPENAI API KEY
OPENAI_API_KEY = env("OPENAI_API_KEY")

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")

JWT_SECRET = env("JWT_SECRET")

# STRIPE_SECRET

STRIPE_PUBLIC_KEY = env("STRIPE_PUBLIC_KEY")
STRIPE_SECRET_KEY = env("STRIPE_SECRET_KEY")
STRIPE_WEBHOOK_SECRET = env("STRIPE_WEBHOOK_SECRET")

# STRIPE PRODUCT AND PRICE IDS
STRIPE_PRODUCT_BASIC_ID = env("STRIPE_PRODUCT_BASIC_ID")
STRIPE_PRICE_BASIC_MONTHLY_ID = env("STRIPE_PRICE_BASIC_MONTHLY_ID")

STRIPE_PRODUCT_PRO_ID = env("STRIPE_PRODUCT_PRO_ID")
STRIPE_PRICE_PRO_MONTHLY_ID = env("STRIPE_PRICE_PRO_MONTHLY_ID")

STRIPE_PRODUCT_ENTERPRISE_ID = env("STRIPE_PRODUCT_ENTERPRISE_ID")
STRIPE_PRICE_ENTERPRISE_MONTHLY_ID = env("STRIPE_PRICE_ENTERPRISE_MONTHLY_ID")


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DEBUG")

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",
    # my apps
    "authentication",
    "core",
    "quiz",
    "tokens",
    "payments",
    "subscriptions",
    "users",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.common.CommonMiddleware",
]

REST_FRAMEWORK = {
    # YOUR SETTINGS
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

ROOT_URLCONF = "backend_ai.urls"

CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = FRONTEND_ORIGINS
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = list(default_headers) + ["authorization", "content-type"]
CORS_ALLOW_METHODS = list(default_methods) + ["PATCH"]

CSRF_TRUSTED_ORIGINS = FRONTEND_ORIGINS

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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

WSGI_APPLICATION = "backend_ai.wsgi.application"


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "PORT": 5432,
        "HOST": "db",
        "USER": env("POSTGRES_USER"),
        "PASSWORD": env("POSTGRES_PASSWORD"),
        "NAME": env("POSTGRES_DB"),
        "OPTIONS": {
            "server_side_binding": True,
        },
    },
}


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

CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
]
CORS_ALLOW_CREDENTIALS = True
# CORS_ALLOW_ALL_ORIGINS = True

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


STATIC_URL = "static/"


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Celery Configuration Options
CELERY_BROKER_URL = os.environ.get("CELERY_BROKER", "redis://redis:6379/0")
CELERY_RESULT_BACKEND = os.environ.get("CELERY_BACKEND", "redis://redis:6379/0")
CELERY_RESULT_EXPIRES = 3600
