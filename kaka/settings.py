"""
Django settings for kaka project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from mongoengine import connect, register_connection, ConnectionError

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

TEST_DB_NAME = 'sandwidge'
TEST_DB_ALIAS = 'test'

PRIMARY_DB_NAME = 'primary'
PRIMARY_DB_ALIAS = 'primary'

connected = False
# connect(PRIMARY_DB_NAME, host='mongodb://10.1.8.102', replicaSet='kaka1')
# MONGODB_HOST = os.environ.get('mongo_PORT_27017_TCP_ADDR', '127.0.0.1')
# connect(host=MONGODB_HOST)
while not connected:
    try:
        connect(PRIMARY_DB_NAME, host='mongodb://mongo')
        connected = True
    except ConnectionError:
        pass

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'd1$!$=ed))z5#11!wz01c)*bpvh$1%a&(t2q0_13g8i4k!ru!v'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True
DEBUG_TOOLBAR_PATCH_SETTINGS = False
INTERNAL_IPS = '10.1.8.120, 127.0.0.1'



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
    'django_extensions',
    'django_tables2',
    'django_tables2_reports',
    'rest_framework',
    'crispy_forms',
    'djorm_pgfulltext',
    'djgeojson',
    #'compressor',
    'async',
    'core',
    'mongcore',
    'seafood',
    'genotype',
    'gene_expression',
    'restless',
    'web',
    'inplaceeditform',
    'experimentsearch',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_tables2_reports.middleware.TableReportMiddleware',
    #'debug_toolbar.middleware.DebugToolbarMiddleware',
)

EXCEL_SUPPORT = 'xlwt'

CRISPY_TEMPLATE_PACK = 'uni_form'

ROOT_URLCONF = 'kaka.urls'

WSGI_APPLICATION = 'kaka.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
   'default': {
        'ENGINE': '',
        # 'NAME': 'postgres',
        # 'USER': 'postgres',
        # 'PORT': '5432',
        # 'HOST': 'db',
    },
#    'default2': {
#        'ENGINE': 'django.db.backends.postgresql_psycopg2',
#        'NAME': 'pionf',
#        'USER': 'pinf',
#        'PORT': '5433',
#        'PASSWORD': 'inkl67z',
#        'HOST': '10.1.8.154',
#    },
#    'test': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#    }
}

SESSION_ENGINE = 'mongoengine.django.sessions'

AUTHENTICATION_BACKENDS = (
    'mongoengine.django.auth.MongoEngineBackend',
)

# TEST_RUNNER = 'experimentsearch.tests.MyTestRunner'

#SOUTH_MIGRATION_MODULES = {
#    'nosql': 'ignore',
#}

#MONGODB_MANAGED_APPS = ['nosql',]
#MONGODB_MANAGED_MODELS = ['ObKV1',]
#DATABASE_ROUTERS = ['django_mongodb_engine.router.MongoDBRouter',]


TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    'django.core.context_processors.request',
)


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
