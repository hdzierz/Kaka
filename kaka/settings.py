"""
Django settings for kaka project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from mongoengine import connect, register_connection

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

TEST_DB_NAME = 'sandwidge'
TEST_DB_ALIAS = 'test'

PRIMARY_DB_NAME = 'primary'
PRIMARY_DB_ALIAS = 'primary'

connected = False
# connect(PRIMARY_DB_NAME, host='mongodb://mongo')
# MONGODB_HOST = os.environ.get('mongo_PORT_27017_TCP_ADDR', '127.0.0.1')
# connect(host=MONGODB_HOST)
#while not connected:
#    try:
#        connect(PRIMARY_DB_NAME, host='mongodb://mongo:27017')
#        connected = True
#    except ConnectionError:
#        pass

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'd1$!$=ed))z5#11!wz01c)*bpvh$1%a&(t2q0_13g8i4k!ru!v'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

DEBUG_TOOLBAR_PATCH_SETTINGS = False
INTERNAL_IPS = '10.1.8.122, 127.0.0.1'



ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #'debug_toolbar',
    #'django.contrib.sites',
    'django_pdb',
    'django_extensions',
    'django_tables2',
    'django_tables2_reports',
    'treebeard',
    'rest_framework',
    'crispy_forms',
    'djorm_pgfulltext',
    'djgeojson',
    #'compressor',
    'raven.contrib.django.raven_compat',
    'django_mongoengine',
    'async',
    'mongcore',
    'mongseafood',
    'mongenotype',
    'mongomarker',
    'gene_expression',
    'restless',
    'web',
    'inplaceeditform',
    'experimentsearch',
)

MIDDLEWARE_CLASSES = (
    'django_pdb.middleware.PdbMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_tables2_reports.middleware.TableReportMiddleware',
    #'debug_toolbar.middleware.DebugToolbarMiddleware',
)


import os
import raven

#RAVEN_CONFIG = {
#    'dsn': 'https://1eccdc5df20c47f6a21ff87975ae7e1a:e3b0ea9be64744d9a2724763fb96a6d5@sentry.io/105726',
    # If you are using git, you can also automatically configure the
    # release based on the git info.
#    'release': raven.fetch_git_sha(os.path.dirname(__file__)),
#}


EXCEL_SUPPORT = 'xlwt'

CRISPY_TEMPLATE_PACK = 'uni_form'

ROOT_URLCONF = 'kaka.urls'

WSGI_APPLICATION = 'kaka.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
#   'default': {
#        'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'postgres',
#         'USER': 'postgres',
#         'PORT': '5432',
#         'HOST': 'db',
#    },
#    'default2': {
#        'ENGINE': 'django.db.backends.postgresql_psycopg2',
#        'NAME': 'pionf',
#        'USER': 'pinf',
#        'PORT': '5433',
#        'PASSWORD': 'inkl67z',
#        'HOST': '10.1.8.154',
#    },
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


SESSION_ENGINE = 'django_mongoengine.sessions'
SESSION_SERIALIZER = 'django_mongoengine.sessions.BSONSerializer'

# TEST_RUNNER = 'experimentsearch.tests.MyTestRunner'

#SOUTH_MIGRATION_MODULES = {
#    'nosql': 'ignore',
#}

#MONGODB_MANAGED_APPS = ['nosql',]
#MONGODB_MANAGED_MODELS = ['ObKV1',]
#DATABASE_ROUTERS = ['django_mongodb_engine.router.MongoDBRouter',]



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
            ]
        },
    },
]


MONGODB_DATABASES = {
    "default": {
        "name": 'primary',
        "host": 'mongo',
        "password": '',
        "username": '',
        "tz_aware": True, # if you using timezones in django (USE_TZ = True)
    },
}




# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Pacific/Auckland'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR 


STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
    "static/",
)
