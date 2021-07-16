# -*- coding: utf-8 -*-
#
# Zephyr documentation build configuration file.
#
# DERIVE and OVERRIDE AS NEEDED from:
# https://github.com/zephyrproject-rtos/zephyr/raw/zephyr-v2.6.0/doc/conf.py
#

import sys
import os
from pathlib import Path
from sphinx.config import eval_config_file

# Paths ------------------------------------------------------------------------

ZEPHYR_BASE = os.environ.get('ZEPHYR_BASE')
if not ZEPHYR_BASE:
    raise ValueError('ZEPHYR_BASE environment variable undefined.')
ZEPHYR_BASE = Path(ZEPHYR_BASE)

ZEPHYR_BUILD = os.environ.get('ZEPHYR_BUILD')
if not ZEPHYR_BUILD:
    raise ValueError('ZEPHYR_BUILD environment variable undefined.')
ZEPHYR_BUILD = Path(ZEPHYR_BUILD)

BRIDLE_BASE = os.environ.get('BRIDLE_BASE')
if not BRIDLE_BASE:
    raise ValueError('BRIDLE_BASE environment variable undefined.')
BRIDLE_BASE = Path(BRIDLE_BASE)

# Add the '_extensions' directory to sys.path, to enable finding Bridle's
# Sphinx extensions within.
sys.path.insert(0, os.path.join(BRIDLE_BASE, 'doc', '_extensions'))

# Add the '_extensions' directory to sys.path, to enable finding Bridle's
# utilities for Sphinx configuration within.
sys.path.insert(0, os.path.join(BRIDLE_BASE, 'doc', '_utils'))
import utils

# pylint: disable=undefined-variable

# General ----------------------------------------------------------------------

# Import all Zephyr configuration, override as needed later
conf = eval_config_file(os.path.join(ZEPHYR_BASE, 'doc', 'conf.py'), tags)
locals().update(conf)

# If your documentation needs a minimal Sphinx version, state it here.
needs_sphinx = '3.3'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions.extend(['sphinx.ext.intersphinx'])
extensions.extend(['bridle.inventory_builder'])

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
# source_suffix = ['.rst', '.md']
source_suffix = '.rst'

# The encoding of source files.
source_encoding = 'utf-8-sig'

# The master toctree document.
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

# The theme that the HTML output should use.
html_theme = 'sphinx_tsn_theme'
html_theme_path = []

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['{}/doc/_static'.format(BRIDLE_BASE),
                    '{}/doc/_static'.format(ZEPHYR_BASE)]

# If not '', a 'Last updated on:' timestamp is inserted at every page bottom,
# using the given strftime format.
html_last_updated_fmt = '%b %d, %Y'

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

# If given, this must be the name of an image file that is the logo of the
# docs, or URL that points an image file for the logo.
html_logo = None

html_context = {
    'show_license': html_show_license,
    'docs_title': docs_title,
    'is_release': is_release,
}

html_theme_options = {
    'docsets': utils.get_docsets('zephyr'),
    'default_docset': utils.get_default_docset(),
}

# Options for intersphinx ------------------------------------------------------

intersphinx_mapping = dict()

kconfig_mapping = utils.get_intersphinx_mapping('kconfig')
if kconfig_mapping:
    intersphinx_mapping['kconfig'] = kconfig_mapping

devicetree_mapping = utils.get_intersphinx_mapping('devicetree')
if devicetree_mapping:
    intersphinx_mapping['devicetree'] = devicetree_mapping

# Options for zephyr.warnings_filter -------------------------------------------

warnings_filter_config = os.path.join(ZEPHYR_BUILD, 'known-warnings.txt')

# Options for external_content -------------------------------------------------

external_content_contents = [
    (ZEPHYR_BASE / 'doc', '[!_]*'),
    (ZEPHYR_BASE, 'boards/**/*.rst'),
    (ZEPHYR_BASE, 'boards/**/doc'),
    (ZEPHYR_BASE, 'samples/**/*.rst'),
    (ZEPHYR_BASE, 'samples/**/doc'),
]


# pylint: enable=undefined-variable

def setup(app):
    app.add_css_file('css/common.css')
    app.add_css_file('css/zephyr.css')
