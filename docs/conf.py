# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys
import django  # Importiere Django

# Füge das Projektverzeichnis zum Python-Suchpfad hinzu
sys.path.insert(0, os.path.abspath('..'))

# Setze die Django-Einstellungsmodule-Umgebungsvariable
os.environ['DJANGO_SETTINGS_MODULE'] = 'first_django_app.settings'  # Pfad zu deinem settings.py

# Initialisiere Django
django.setup()

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'First_Django_Projekt'
copyright = '2024, Safa Shamari'
author = 'Safa Shamari'
release = '2025'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',  # Aktiviert autodoc-Erweiterung
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
