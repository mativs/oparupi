import os
SITE_ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

COMPASS_INPUT = os.path.join(SITE_ROOT, 'static/sass')
COMPASS_OUTPUT = os.path.join(SITE_ROOT, 'static/css')
COMPASS_IMAGE_DIR = os.path.join(SITE_ROOT, 'static/img')
COMPASS_SCRIPT_DIR = os.path.join(SITE_ROOT, 'static/js')
COMPASS_STYLE = 'compact'
COMPASS_REQUIRES = (
    'zurb-foundation',  
)