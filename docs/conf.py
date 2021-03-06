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
from datetime import datetime
from pathlib import Path
from typing import Optional

try:
    import codestyle
except ModuleNotFoundError:
    import sys
    sys.path.insert(0, str(Path().absolute().parent))
finally:
    from codestyle import (__author__ as codestyle_author,
                           __version__ as codestyle_version,
                           __url__ as codestyle_url)


PROJECT_PATH = Path().absolute().parent


# -- Project information -----------------------------------------------------

project = PROJECT_PATH.name
author = codestyle_author
copyright = f'{datetime.now().year}, {author}'

# The full version, including alpha/beta/rc tags
release = codestyle_version

# The short X.Y version
version = '.'.join(codestyle_version.split('.')[0:2])


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.todo',
    'sphinx.ext.intersphinx',
    'sphinx.ext.coverage',
    'sphinx.ext.linkcode',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = 'ru'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'alabaster'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = []


# -- Extension configuration -------------------------------------------------
autodoc_mock_imports = ['configargparse']

# -- Options for intersphinx extension ---------------------------------------

# Example configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {'https://docs.python.org/3/': None}

# -- Options for todo extension ----------------------------------------------

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = True


def linkcode_resolve(domain: str, info: dict) -> Optional[str]:
    """
    URL to source code corresponding to the object in given domain.

    https://www.sphinx-doc.org/en/master/usage/extensions/linkcode.html

    :param domain: language domain the object is in.
    :param info: is a dictionary with the following keys guaranteed to
        be present (dependent on the domain).
    :return: URL to source code.
    """
    if info['module'] and domain == 'py':
        filename = info['module'].replace('.', '/')
        return f'{codestyle_url}/-/blob/master/{filename}.{domain}'
