import os
import sys

sys.path.insert(0, os.path.abspath('..'))  # Add project root to path

import django
os.environ['DJANGO_SETTINGS_MODULE'] = 'fitnessproject.settings'
django.setup()

extensions = ['sphinx.ext.autodoc', 'sphinx.ext.viewcode']
