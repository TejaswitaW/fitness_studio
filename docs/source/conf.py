import os
import sys
import django

# Add project root to sys.path so autodoc can find your Django apps
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# Set DJANGO_SETTINGS_MODULE environment variable
os.environ['DJANGO_SETTINGS_MODULE'] = 'fitnessproject.settings'  # Adjust if needed

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
    # Uncomment below if you use Google or NumPy style docstrings
    # 'sphinx.ext.napoleon',
]

templates_path = ['_templates']
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------

html_theme = 'alabaster'  # Or 'sphinx_rtd_theme' if you want to use ReadTheDocs theme
html_static_path = ['_static']
