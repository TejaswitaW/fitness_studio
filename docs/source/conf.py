import os
import sys
import django

# Get the absolute path to the Django project root (where manage.py is)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

# Set the Django settings module
os.environ['DJANGO_SETTINGS_MODULE'] = 'fitnessproject.settings'

# Setup Django
django.setup()

# -- Project information -----------------------------------------------------
project = 'Fitness Studio'
copyright = '2025, Tejaswita Wakhure'
author = 'Tejaswita Wakhure'
release = '1.0.0'

# -- General configuration ---------------------------------------------------
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    # 'sphinx.ext.napoleon',  # Uncomment if using Google-style docstrings
    # 'myst_parser',  # Uncomment if using Markdown files
]

templates_path = ['_templates']
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
html_theme = 'alabaster'
html_static_path = ['_static']
