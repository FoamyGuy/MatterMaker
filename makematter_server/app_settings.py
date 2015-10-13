import os


APP_ROOT = os.path.dirname(__file__)


MEDIA_ROOT = os.path.join(APP_ROOT, 'media')
MEDIA_URL = '/media/'
MEDIA_OUT = os.path.join(MEDIA_ROOT, 'out')

WORKING_DIR = os.path.join(APP_ROOT, "tmp")