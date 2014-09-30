import os, random

MEMEX_API_VERSION = "0.1"

HBASE_HOST = random.choice(os.environ.get('HBASE_HOST', 'localhost').split(','))
HBASE_PREFIX = os.environ['HBASE_PREFIX']

try:
    if os.environ['APPLICATION_ENV'] is 'production':
        DEBUG = False   
    else:
        DEBUG = True
except:
    DEBUG = True

TEMPLATE_DEBUG = DEBUG

ADMINS = ()

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', 
        'NAME': 'web', 
        'USER': '',
        'PASSWORD': '', 
        'HOST': '',
        'PORT': '',
    },
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'cache_data',
    }
}

ALLOWED_HOSTS = ['*']

TIME_ZONE = 'America/Los_Angeles'

LANGUAGE_CODE = 'en-us'

SITE_ID = 1

USE_I18N = True

USE_L10N = True

MEDIA_ROOT = ''

MEDIA_URL = ''

#STATIC_ROOT = '/home/marti/memexapi/public/static'

#STATIC_URL = '/static/'

#ADMIN_MEDIA_PREFIX = '/static/admin/'

STATICFILES_DIRS = (
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

SECRET_KEY = '8w!qq4)&7&7!o+62jo(#5^mk#+iims0+7h8&n3wf_nuks&unc5'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'api.urls'

TEMPLATE_DIRS = (
#    '/home/marti/memexapi/public',
)

INSTALLED_APPS = (
    'api',
    #'rest_framework',
    'django.contrib.sessions',
    #'django.contrib.auth',
    #'django.contrib.contenttypes',
    #'django.contrib.sites',
    #'django.contrib.messages',
    #'django.contrib.staticfiles',
    #'django.contrib.admin',
    #'django.contrib.admindocs',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
