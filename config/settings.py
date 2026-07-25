import os
from pathlib import Path
from dotenv import load_dotenv, dotenv_values

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env')

SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-change-me-in-production')
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms',
    'crispy_tailwind',
    'django_filters',
    'apps.accounts',
    'apps.core',
    'apps.filiais',
    'apps.professores',
    'apps.alunos',
    'apps.convites',
    'apps.parametros',
    'apps.relatorios',
    'apps.midia',
    'apps.rede',
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

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': os.getenv('DB_ENGINE', 'django.db.backends.mysql'),
        'NAME': os.getenv('DB_NAME', 'avante'),
        'USER': os.getenv('DB_USER', 'avante'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'avante'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '3306'),
    }
}

if os.getenv('DB_ENGINE', '').startswith('mysql'):
    DATABASES['default']['OPTIONS'] = {
        'charset': 'utf8mb4',
        'init_command': "SET sql_mode='STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION'",
    }

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = os.getenv('LANGUAGE_CODE', 'pt-br')
TIME_ZONE = os.getenv('TIME_ZONE', 'America/Sao_Paulo')
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'accounts.User'
LOGIN_URL = 'accounts:login'
LOGIN_REDIRECT_URL = 'core:dashboard'
LOGOUT_REDIRECT_URL = 'accounts:login'

CRISPY_ALLOWED_TEMPLATE_PACKS = 'tailwind'
CRISPY_TEMPLATE_PACK = 'tailwind'

_env_file = dotenv_values(BASE_DIR / '.env')
BREVO_API_KEY = _env_file.get('BREVO_API_KEY') or os.getenv('BREVO_API_KEY', '')
_DEFAULT_EMAIL_BACKEND = 'apps.core.brevo_email_backend.BrevoAPIEmailBackend' if BREVO_API_KEY else 'django.core.mail.backends.console.EmailBackend'
EMAIL_BACKEND = _env_file.get('EMAIL_BACKEND') or os.getenv('EMAIL_BACKEND', _DEFAULT_EMAIL_BACKEND)
EMAIL_HOST = _env_file.get('EMAIL_HOST') or os.getenv('EMAIL_HOST', '')
EMAIL_PORT = int(_env_file.get('EMAIL_PORT') or os.getenv('EMAIL_PORT', '587'))
EMAIL_HOST_USER = _env_file.get('EMAIL_HOST_USER') or os.getenv('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = _env_file.get('EMAIL_HOST_PASSWORD') or os.getenv('EMAIL_HOST_PASSWORD', '')
EMAIL_USE_TLS = (_env_file.get('EMAIL_USE_TLS') or os.getenv('EMAIL_USE_TLS', 'True')).lower() == 'true'
DEFAULT_FROM_EMAIL = _env_file.get('DEFAULT_FROM_EMAIL') or os.getenv('DEFAULT_FROM_EMAIL', 'avante <avantebrazilianjj@gmail.com>')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}
