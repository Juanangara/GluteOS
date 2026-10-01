import os
from pathlib import Path

from django.core.exceptions import ImproperlyConfigured

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


def _cargar_env(ruta):
    """Carga variables KEY=VALUE desde un archivo .env, sin dependencias externas.
    Las variables ya definidas en el entorno tienen prioridad."""
    if not ruta.exists():
        return
    for linea in ruta.read_text(encoding="utf-8").splitlines():
        linea = linea.strip()
        if not linea or linea.startswith("#") or "=" not in linea:
            continue
        clave, valor = linea.split("=", 1)
        os.environ.setdefault(clave.strip(), valor.strip().strip('"').strip("'"))


def _env(nombre, por_defecto=None):
    valor = os.environ.get(nombre, por_defecto)
    if valor is None:
        raise ImproperlyConfigured(
            f"Falta la variable de entorno {nombre}. Copia Project/.env.example a Project/.env."
        )
    return valor


_cargar_env(BASE_DIR / ".env")


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = _env("DJANGO_SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = _env("DJANGO_DEBUG", "False").lower() == "true"

ALLOWED_HOSTS = [h.strip() for h in _env("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1").split(",") if h.strip()]


# Application definition

INSTALLED_APPS = [
    # Default contrib apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    #Project/apps
    'apps.socios',
    'apps.pagos',
    'apps.seguridad',
    'apps.control_acceso',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # Busca plantillas en BASE_DIR / "templates" además de app templates
        'DIRS': [ BASE_DIR / 'templates' ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',     
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'Project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

# CONFIGURACIÓN PARA POSTGRESQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': _env('POSTGRES_DB'),
        'USER': _env('POSTGRES_USER'),
        'PASSWORD': _env('POSTGRES_PASSWORD'),
        'HOST': _env('POSTGRES_HOST', 'localhost'),
        'PORT': _env('POSTGRES_PORT', '5432'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'es-co'

# Ajustado a tu zona horaria (Colombia)
TIME_ZONE = 'America/Bogota'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'
# opcional: si quieres servir assets locales en dev desde BASE_DIR/static
# STATICFILES_DIRS = [ BASE_DIR / "static" ]

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



# QUITARRRRRR (LO USEO SOLO PARA TESTING)
import sys

if "test" in sys.argv:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": ":memory:",
        }
    }
