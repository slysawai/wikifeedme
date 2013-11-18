import os
import sys

sys.path.append('/home/dnaber/djangosite/djangosite')
sys.path.append('/home/dnaber/djangosite/wikifeedme')
sys.path.append('/home/dnaber/djangosite')

os.environ['PYTHON_EGG_CACHE'] = '/home/dnaber/djangosite/wikifeedme/.python-egg'
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
