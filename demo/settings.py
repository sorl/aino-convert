from os.path import dirname, join as pjoin

DEBUG = True
TEMPLATE_DEBUG = DEBUG
CONVERT_DEBUG = DEBUG
MEDIA_ROOT = pjoin(dirname(__file__), 'media')
MEDIA_URL = '/media/'
ADMIN_MEDIA_PREFIX = '/adminmedia/'
ROOT_URLCONF = 'demo.urls'
TEMPLATE_DIRS = pjoin(dirname(__file__), 'templates'),
INSTALLED_APPS = 'convert',
