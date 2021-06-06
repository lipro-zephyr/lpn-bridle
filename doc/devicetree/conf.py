# -*- coding: utf-8 -*-
#
# COPIED and CHANGED from:
# https://github.com/zephyrproject-rtos/zephyr/raw/zephyr-v2.5.0/doc/conf.py
#
# Devicetree bindings build configuration file, created by
# sphinx-quickstart on Fri May  8 11:43:01 2015.
#
# This file is execfile()d with the current directory set to its
# containing dir.
#
# Note that not all possible configuration values are present in this
# autogenerated file.
#
# All configuration values have a default; values that are commented out
# serve to show the default.

import sys
import os

if "ZEPHYR_BASE" not in os.environ:
    sys.exit("$ZEPHYR_BASE environment variable undefined.")
ZEPHYR_BASE = os.path.abspath(os.environ["ZEPHYR_BASE"])

if "ZEPHYR_BUILD" not in os.environ:
    sys.exit("$ZEPHYR_BUILD environment variable undefined.")
ZEPHYR_BUILD = os.path.abspath(os.environ["ZEPHYR_BUILD"])

if "ZEPHYR_OUTPUT" not in os.environ:
    sys.exit("$ZEPHYR_OUTPUT environment variable undefined.")
ZEPHYR_OUTPUT = os.path.abspath(os.environ["ZEPHYR_OUTPUT"])

if "DTS_BINDINGS_OUTPUT" not in os.environ:
    print ("DTS_BINDINGS_OUTPUT")
    sys.exit("$DTS_BINDINGS_OUTPUT environment variable undefined.")
DTS_BINDINGS_OUTPUT = os.path.abspath(os.environ["DTS_BINDINGS_OUTPUT"])

if "BRIDLE_BASE" not in os.environ:
    print ("BRIDLE_BASE")
    sys.exit("$BRIDLE_BASE environment variable undefined.")
BRIDLE_BASE = os.path.abspath(os.environ["BRIDLE_BASE"])

# -- General configuration ------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.intersphinx',
#   'breathe', 'sphinx.ext.todo',
#   'sphinx.ext.extlinks',
#   'sphinx.ext.autodoc',
#   'zephyr.application',
#   'zephyr.html_redirects',
#   'only.eager_only',
#   'zephyr.link-roles',
    'sphinx_tabs.tabs'
]

# Sphinx 2.0 changes the default from 'index' to 'contents'
master_doc = 'index'

# General information about the project.
project = u'Devicetree Bindings'
copyright = u'2019-2021 TiaC Systems members and individual contributors'
author = u'TiaC Systems'

# Get rid of version number while keeping the spacing the same as for other
# docsets
version = '&nbsp;'

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = None

# There are two options for replacing |today|: either, you set today to some
# non-false value, then it is used:
#today = ''
# Else, today_fmt is used as the format for a strftime call.
#today_fmt = '%B %d, %Y'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = ['_build']

# -- Options for HTML output ----------------------------------------------

### by TiaC ###
html_theme = "devicetree"
html_theme_path = ['{}/doc/themes'.format(BRIDLE_BASE)]
### by TiaC ###

# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".
html_title = "Devicetree Bindings"

# This value determines the text for the permalink; it defaults to "¶".
# Set it to None or the empty string to disable permalinks.
#html_add_permalinks = ""

# A shorter title for the navigation bar.  Default is the same as html_title.
#html_short_title = None

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
### OFF by TiaC ### html_logo = 'images/Zephyr-Kite-logo.png'

# The name of an image file (within the static path) to use as favicon of the
# docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
### OFF by TiaC ### html_favicon = 'images/zp_favicon.png'
html_favicon = '{}/doc/static/images/lpn.ico'.format(BRIDLE_BASE)  ### by TiaC ###

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['{}/doc/static'.format(BRIDLE_BASE)]

# Add any extra paths that contain custom files (such as robots.txt or
# .htaccess) here, relative to this directory. These files are copied
# directly to the root of the documentation.
#html_extra_path = []

# If not '', a 'Last updated on:' timestamp is inserted at every page bottom,
# using the given strftime format.
html_last_updated_fmt = '%b %d, %Y'

# If true, SmartyPants will be used to convert quotes and dashes to
# typographically correct entities.
#html_use_smartypants =

# Custom sidebar templates, maps document names to template names.
#html_sidebars = {}

# Additional templates that should be rendered to pages, maps page names to
# template names.
#html_additional_pages = {}

# If false, no module index is generated.
html_domain_indices = False

# If false, no index is generated.
html_use_index = True

# If true, the index is split into individual pages for each letter.
html_split_index = True

# If true, links to the reST sources are added to the pages.
html_show_sourcelink = False

# If true, "Created using Sphinx" is shown in the HTML footer. Default is True.
html_show_sphinx = False

# If true, "(C) Copyright ..." is shown in the HTML footer. Default is True.
html_show_copyright = True

# If true, license is shown in the HTML footer. Default is True.
html_show_license = True

# If true, an OpenSearch description file will be output, and all pages will
# contain a <link> tag referring to it.  The value of this option must be the
# base URL from which the finished HTML is served.
#html_use_opensearch = ''

# This is the file name suffix for HTML files (e.g. ".xhtml").
#html_file_suffix = None

# Language to be used for generating the HTML full-text search index.
# Sphinx supports the following languages:
#   'da', 'de', 'en', 'es', 'fi', 'fr', 'hu', 'it', 'ja'
#   'nl', 'no', 'pt', 'ro', 'ru', 'sv', 'tr'
#html_search_language = 'en'

sourcelink_suffix = '.txt'

# A dictionary with options for the search language support, empty by default.
# Now only 'ja' uses this config value
#html_search_options = {'type': 'default'}

# The name of a javascript file (relative to the configuration directory) that
# implements a search results scorer. If empty, the default will be used.
### OFF by TiaC ### html_search_scorer = 'scorer.js'

intersphinx_mapping = {
    # python -m sphinx.ext.intersphinx objects.inv | less
    # 'designator': (target link base, inventory file)
    'zephyr': (os.path.relpath(ZEPHYR_OUTPUT, DTS_BINDINGS_OUTPUT),
               os.path.join(BRIDLE_BASE, 'doc', 'devicetree',
                            'zephyr_objects.inv')),
}

def setup(app):
    app.add_css_file("css/common.css")  ### by TiaC ###
    app.add_css_file("css/devicetree.css")  ### by TiaC ###
    app.add_js_file("js/bridle.js")  ### by TiaC ###
