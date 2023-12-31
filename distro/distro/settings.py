from pathlib import Path
import os
from redis import Redis
from rq import Queue
import configparser
import dj_database_url


config = configparser.ConfigParser()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

config.read(os.path.dirname(os.path.abspath(BASE_DIR)) + '/config.cfg')

TASK_RETRIES = int(config.get('configurations', 'task_retries'))

if config.get('configurations', 'modules_path') == 'default':
    MODULES_PATH = os.path.join(os.path.dirname(os.path.abspath(os.getcwd())), 'modules')
else:
    MODULES_PATH = config.get('configurations', 'modules_path')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'secreto'

# SECURITY WARNING: don't run with debug turned on in production!
if int(os.environ.get('DEBUG')) == 1:
    DEBUG = True
    REDIS_URL = 'rediss://red-clu2rjla73kc7398rbn0:HrGmkzsLFmjDcDSLESGUBJrmw0Dv9bgL@ohio-redis.render.com:6379'
    database_cfg = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
else:
    DEBUG = False
    database_cfg = dj_database_url.parse(config.get('configurations', 'postgre_url'))
    REDIS_URL = 'redis://host.docker.internal:6379'


ALLOWED_HOSTS = ['*']

REDIS_CONNECTION = Redis.from_url(REDIS_URL)


DEFAULT_QUEUE = Queue(name='default', connection=REDIS_CONNECTION)
LOW_QUEUE = Queue(name='low', connection=REDIS_CONNECTION)
HIGH_QUEUE = Queue(name='high', connection=REDIS_CONNECTION)

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
]

INSTALLED_APPS += [
    'scheduler',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = 'distro.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'distro.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': database_cfg
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

APPEND_SLASH = False

CORS_ORIGIN_ALLOW_ALL = True

