import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'api.settings'
os.environ['HBASE_HOST'] = '127.0.0.1'
os.environ['HBASE_PREFIX'] = 'memex_'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
