# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
from datetime import date
import pathlib
import sys

ROOT_DIR = pathlib.Path(__file__).parent.parent.parent.resolve()
print(ROOT_DIR)

sys.path.insert(0, str(ROOT_DIR / 'src'))

# -- Project information -----------------------------------------------------

project = 'asyncio nats service'
copyright = f'{date.today().year}, Victor Borisov <borisov@borisovcode.com>, Konstantin Paltsev <enotukit@gmail.com>'
author = 'Victor Borisov <borisov@borisovcode.com>, Konstantin Paltsev <enotukit@gmail.com>'

about = {}
exec((ROOT_DIR / 'src' / 'asyncio_nats_service' / '__version__.py').read_text(encoding='utf-8'), about)

version = about['__version__']
# The full version, including alpha/beta/rc tags
release = version

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx.ext.viewcode',
    # 'sphinx.ext.napoleon',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build"]

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'alabaster'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

intersphinx_mapping = {"python": ("https://docs.python.org/3", None)}
