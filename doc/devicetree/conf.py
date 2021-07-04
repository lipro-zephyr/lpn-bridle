# -*- coding: utf-8 -*-
#
# COPIED and CHANGED from:
# https://github.com/zephyrproject-rtos/zephyr/raw/zephyr-v2.6.0/doc/conf.py
#

import sys
import os
from pathlib import Path

# Paths ------------------------------------------------------------------------

ZEPHYR_BASE = os.environ.get('ZEPHYR_BASE')
if not ZEPHYR_BASE:
    raise ValueError('ZEPHYR_BASE environment variable undefined.')
ZEPHYR_BASE = Path(ZEPHYR_BASE)

BRIDLE_BASE = os.environ.get('BRIDLE_BASE')
if not BRIDLE_BASE:
    raise ValueError('BRIDLE_BASE environment variable undefined.')
BRIDLE_BASE = Path(BRIDLE_BASE)

# Add the 'extensions' directory to sys.path, to enable finding Zephyr's
# Sphinx extensions within.
sys.path.insert(0, os.path.join(ZEPHYR_BASE, 'doc', '_extensions'))

# Add the '_extensions' directory to sys.path, to enable finding Bridle's
# Sphinx extensions within.
sys.path.insert(0, os.path.join(BRIDLE_BASE, 'doc', '_extensions'))

# Add the '_extensions' directory to sys.path, to enable finding Bridle's
# utilities for Sphinx configuration within.
sys.path.insert(0, os.path.join(BRIDLE_BASE, 'doc', '_utils'))
import utils

# Project ----------------------------------------------------------------------

# General information about the project.
project = u'Devicetree Bindings'
copyright = u'2019-2021 TiaC Systems members and individual contributors'
author = u'TiaC Systems'

# Get rid of version number while keeping the spacing the same as for other
# docsets
version = '&nbsp;'

# General ----------------------------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
needs_sphinx = '3.3'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx.ext.extlinks',
    'sphinx.ext.ifconfig',
    'sphinx_tabs.tabs',
    'only.eager_only',
    'notfound.extension',
    'zephyr.dtcompatible-role',
    'zephyr.external_content',
    'bridle.inventory_builder',
]

# Only use SVG converter when it is really needed, e.g. LaTeX.
if tags.has('svgconvert'):  # pylint: disable=undefined-variable
    extensions.append('sphinxcontrib.rsvgconverter')

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
# source_suffix = ['.rst', '.md']
source_suffix = '.rst'

# The encoding of source files.
source_encoding = 'utf-8-sig'

# Sphinx 2.0 changes the default from 'index' to 'contents'
master_doc = 'index'

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = None

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# If this is True, todo and todolist produce output, else they produce nothing.
# The default is False.
todo_include_todos = False

# Options for HTML output ------------------------------------------------------

# TODO / FIXME : Build, deploy and use her a customized Sphinx theme
### NOT YET ### html_theme = 'sphinx_tsn_theme'
html_theme = 'devicetree'
html_theme_path = ['{}/doc/_themes'.format(BRIDLE_BASE)]
### NOT YET ### html_theme_options = {'docsets': utils.get_docsets('devicetree')}
html_theme_options = {
    'logo_only': True,
    'prev_next_buttons_location': 'bottom',
    'style_external_links': True,
}

# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".
html_title = project

# The name of an image file (within the static path) to use as favicon of the
# docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
html_favicon = '{}/doc/_static/images/bridle.ico'.format(BRIDLE_BASE)

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['{}/doc/_static'.format(BRIDLE_BASE)]

# If not '', a 'Last updated on:' timestamp is inserted at every page bottom,
# using the given strftime format.
html_last_updated_fmt = '%b %d, %Y'

# If false, no module index is generated.
html_domain_indices = False

# If false, no index is generated.
html_use_index = True

# If true, the index is split into individual pages for each letter.
html_split_index = True

# If true, links to the reST sources are added to the pages.
html_show_sourcelink = True

# If true, "Created using Sphinx" is shown in the HTML footer. Default is True.
html_show_sphinx = False

# If true, "(C) Copyright ..." is shown in the HTML footer. Default is True.
html_show_copyright = True

# If true, license is shown in the HTML footer. Default is True.
html_show_license = True

# Options for intersphinx ------------------------------------------------------

intersphinx_mapping = dict()

zephyr_mapping = utils.get_intersphinx_mapping('zephyr')
if zephyr_mapping:
    intersphinx_mapping['zephyr'] = zephyr_mapping

# Options for zephyr.external_content ------------------------------------------

external_content_directives = (
    'figure',
    'image',
    'include',
    'literalinclude',
)
external_content_contents = [
    (BRIDLE_BASE / 'doc' / 'devicetree', '[!_]*'),
]
external_content_keep = [
    'bindings.rst',
    'bindings/**/*',
    'compatibles/**/*',
]


def setup(app):
    app.add_css_file('css/common.css')
    app.add_css_file('css/devicetree.css')
