# Configuration file for the Sphinx documentation builder.

import os
import sys
import re
sys.path.insert(0, os.path.abspath('..'))
import revitron_sphinx_theme

# -- Project information -----------------------------------------------------
project = 'stackit'
copyright = '2025, Edoardo Balducci'
author = 'Edoardo Balducci'
slug = re.sub(r'\W+', '-', project.lower())

# The full version, including alpha/beta/rc tags
# release = '0.2.0'
# version = '0.2.0'

# -- General configuration ---------------------------------------------------
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'revitron_sphinx_theme',
    'autodocsumm'
]

autodoc_default_options = {
    'autosummary': True
}

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
master_doc = 'index'

# -- Options for HTML output -------------------------------------------------
html_theme = "revitron_sphinx_theme"

# Theme options
html_theme_options = {
    'navigation_depth': 5,
    'github_url': 'https://github.com/bbalduzz/stackit',
    'logo_mobile': 'stackit-logo-dark.png',
    'color_scheme': 'light'
}

# Landing page configuration
html_context = {
    'landing_page': {
        'menu': [
            {'title': 'Documentation', 'url': 'installation.html'},
            {'title': 'Quick Start', 'url': 'quickstart.html'},
            {'title': 'API Reference', 'url': 'api/index.html'},
        ]
    }
}

html_logo = 'stackit-logo-dark.png'
html_title = 'StaKit'  # Empty to hide text, show only logo
html_show_sourcelink = True
htmlhelp_basename = slug

# Only use static files if they exist
if os.path.exists(os.path.join(os.path.dirname(__file__), '_static')):
    html_static_path = ['_static']
    html_css_files = ['custom.css']
else:
    html_static_path = []

# -- Extension configuration -------------------------------------------------
# Napoleon settings
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_preprocess_types = False
napoleon_type_aliases = None
napoleon_attr_annotations = True

# Intersphinx configuration
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
}

# Todo extension
todo_include_todos = True
