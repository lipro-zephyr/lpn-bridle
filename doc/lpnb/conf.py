#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# COPIED and CHANGED from:
# https://github.com/zephyrproject-rtos/zephyr/raw/zephyr-v2.5.0/doc/conf.py
#
# Li-Pro.Net bridle documentation build configuration file, created by
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

if "ZEPHYR_RST_SRC" not in os.environ:
    sys.exit("$ZEPHYR_RST_SRC environment variable undefined.")
ZEPHYR_RST_SRC = os.path.abspath(os.environ["ZEPHYR_RST_SRC"])

if "KCONFIG_OUTPUT" not in os.environ:
    sys.exit("$KCONFIG_OUTPUT environment variable undefined.")
KCONFIG_OUTPUT = os.path.abspath(os.environ["KCONFIG_OUTPUT"])

if "DTS_BINDINGS_OUTPUT" not in os.environ:
    print ("DTS_BINDINGS_OUTPUT")
    sys.exit("$DTS_BINDINGS_OUTPUT environment variable undefined.")
DTS_BINDINGS_OUTPUT = os.path.abspath(os.environ["DTS_BINDINGS_OUTPUT"])

if "LPNB_BASE" not in os.environ:
    sys.exit("$LPNB_BASE environment variable undefined.")
LPNB_BASE = os.path.abspath(os.environ["LPNB_BASE"])

if "LPNB_BUILD" not in os.environ:
    sys.exit("$LPNB_BUILD environment variable undefined.")
LPNB_BUILD = os.path.abspath(os.environ["LPNB_BUILD"])

if "LPNB_OUTPUT" not in os.environ:
    sys.exit("$LPNB_OUTPUT environment variable undefined.")
LPNB_OUTPUT = os.path.abspath(os.environ["LPNB_OUTPUT"])

if "LPNB_RST_SRC" not in os.environ:
    sys.exit("$LPNB_RST_SRC environment variable undefined.")
LPNB_RST_SRC = os.path.abspath(os.environ["LPNB_RST_SRC"])

# Add the 'extensions' directory to sys.path, to enable finding Sphinx
# extensions within.
sys.path.insert(0, os.path.join(ZEPHYR_BASE, 'doc', 'extensions'))

# Let Sphinx find our extensions.
sys.path.append(os.path.join(LPNB_BASE, 'scripts', 'sphinx_extensions'))

# Add the directory which contains the runners package as well,
# for autodoc directives on runners.xyz.
sys.path.insert(0, os.path.join(ZEPHYR_BASE, 'scripts', 'west_commands'))

try:
    import west as west_found
except ImportError:
    west_found = False

# -- General configuration ------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#
# needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.intersphinx',
    'breathe',
    'interbreathe',
#   'table_from_rows',
    'options_from_kconfig',
#   'lpn_include',
#   'sphinx.ext.todo',
#   'sphinx.ext.extlinks',
#   'sphinx.ext.autodoc',
    'sphinx.ext.ifconfig',
    'sphinxcontrib.mscgen',
    'sphinx_tabs.tabs',
    'zephyr.application',
    'zephyr.html_redirects',
#   'only.eager_only',
    'zephyr.link-roles',
    'crate.sphinx.csv',
]

# Only use SVG converter when it is really needed, e.g. LaTeX.
if tags.has("svgconvert"):
    extensions.append('sphinxcontrib.rsvgconverter')

# Add any paths that contain templates here, relative to this directory.
### OFF by LPNB ### templates_path = ['_templates']

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
# source_suffix = ['.rst', '.md']
source_suffix = '.rst'

# The encoding of source files.
#source_encoding = 'utf-8-sig'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = u'Li-Pro.Net bridle'
copyright = u'2019-2021 Li-Pro.Net members and individual contributors'
author = u'Li-Pro.Net'

# The following code tries to extract the information by reading the Makefile,
# when Sphinx is run directly (e.g. by Read the Docs).
try:
    version_major = None
    version_minor = None
    patchlevel = None
    extraversion = None
    for line in open(os.path.join(LPNB_BASE, 'VERSION')):
        key, val = [x.strip() for x in line.split('=', 2)]
        if key == 'VERSION_MAJOR':
            version_major = val
        if key == 'VERSION_MINOR':
            version_minor = val
        elif key == 'PATCHLEVEL':
            patchlevel = val
        elif key == 'EXTRAVERSION':
            extraversion = val
        if version_major and version_minor and patchlevel and extraversion:
            break
except Exception:
    pass
finally:
    if version_major and version_minor and patchlevel and extraversion is not None:
        version = release = version_major + '.' + version_minor + '.' + patchlevel
        if extraversion != '':
            version = release = version + '-' + extraversion
    else:
        sys.exit("Could not extract LPNB version.")

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
# This patterns also effect to html_static_path and html_extra_path
exclude_patterns = ['_build']
if not west_found:
    exclude_patterns.append('**/*west-apis*')
else:
    exclude_patterns.append('**/*west-not-found*')

# The reST default role (used for this markup: `text`) to use for all
# documents.

# This change will allow us to use bare back-tick notation to let
# Sphinx hunt for a reference, starting with normal "document"
# references such as :ref:, but also including :c: and :cpp: domains
# (potentially) helping with API (doxygen) references simply by using
# `name`

default_role = 'any'
# default_domain = 'cpp'

# If true, '()' will be appended to :func: etc. cross-reference text.
#add_function_parentheses = True

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
#add_module_names = True

# If true, sectionauthor and moduleauthor directives will be shown in the
# output. They are ignored by default.
#show_authors = False

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# Additional lexer for Pygments (syntax highlighting)
from lexer.DtsLexer import DtsLexer
from sphinx.highlighting import lexers
lexers['DTS'] = DtsLexer()

# A list of ignored prefixes for module index sorting.
#modindex_common_prefix = []

# If true, keep warnings as "system message" paragraphs in the built documents.
#keep_warnings = False

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = False

rst_prolog = """
.. include:: /roles.txt
"""

rst_epilog = """
.. include:: /links.txt
.. include:: /shortcuts.txt
.. include:: /versions.txt
"""

# -- Options for HTML output ----------------------------------------------

### OFF by LPNB ### import sphinx_rtd_theme
### OFF by LPNB ### html_theme = "sphinx_rtd_theme"
### OFF by LPNB ### html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
### OFF by LPNB ### html_theme_options = {
### OFF by LPNB ###     'prev_next_buttons_location': None
### OFF by LPNB ### }

### by LPNB ###
html_theme = 'lpnb'
html_theme_path = ['{}/doc/themes'.format(LPNB_BASE)]
### by LPNB ###

if tags.has('release'):  # pylint: disable=undefined-variable
    is_release = True
    docs_title = 'Docs / %s' %(version)
else:
    is_release = False
    docs_title = 'Docs / Latest'

# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".
html_title = "Li-Pro.Net bridle to embedded environment"

# This value determines the text for the permalink; it defaults to "¶".
# Set it to None or the empty string to disable permalinks.
#html_add_permalinks = ""

# A shorter title for the navigation bar.  Default is the same as html_title.
#html_short_title = None

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
### OFF by LPNB ### html_logo = 'images/Zephyr-Kite-logo.png'

# The name of an image file (within the static path) to use as favicon of the
# docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
### OFF by LPNB ### html_favicon = 'images/zp_favicon.png'
html_favicon = '{}/doc/static/images/lpn.ico'.format(LPNB_BASE)  ### by LPNB ###

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
### OFF by LPNB ### html_static_path = ['{}/doc/static'.format(ZEPHYR_BASE)]
html_static_path = ['{}/doc/static'.format(LPNB_BASE)]

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
html_show_copyright = True  ### by LPNB ###

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
### OFF by LPNB ### html_search_scorer = 'scorer.js'

# Link the Kconfig docs with Intersphinx so that references to Kconfig symbols
# (via :option:`CONFIG_FOO`) turn into links
intersphinx_mapping = {
    # python -m sphinx.ext.intersphinx objects.inv | less
    # 'designator': (target link base, inventory file)
    'kconfig': (os.path.relpath(KCONFIG_OUTPUT, LPNB_OUTPUT),
                os.path.join(os.path.relpath(KCONFIG_OUTPUT, LPNB_RST_SRC),
                             'objects.inv')),
    'dtsbind': (os.path.relpath(DTS_BINDINGS_OUTPUT, LPNB_OUTPUT),
                os.path.join(os.path.relpath(DTS_BINDINGS_OUTPUT, LPNB_RST_SRC),
                             'objects.inv')),
    'zephyr': (os.path.relpath(ZEPHYR_OUTPUT, LPNB_OUTPUT),
               os.path.join(os.path.relpath(ZEPHYR_OUTPUT, LPNB_RST_SRC),
                            'objects.inv')),
}

breathe_projects = {
    "lpnb": "{}/doxygen/xml".format(LPNB_BUILD),
}
breathe_default_project = "lpnb"

breathe_domain_by_extension = {
    "h": "c",
    "c": "c",
}
breathe_separate_member_pages = True
breathe_show_enumvalue_initializer = True

# Qualifiers to a function are causing Sphihx/Breathe to warn about
# Error when parsing function declaration and more.  This is a list
# of strings that the parser additionally should accept as
# attributes.
cpp_id_attributes = [
    '__syscall', '__deprecated', '__may_alias',
    '__used', '__unused', '__weak',
    '__DEPRECATED_MACRO', 'FUNC_NORETURN',
    '__subsystem',
]
c_id_attributes = cpp_id_attributes

def setup(app):
    app.add_css_file("css/colors.css")  ### by LPNB ###
    app.add_css_file("css/strikethrough.css")  ### by LPNB ###
    app.add_css_file("css/underline.css")  ### by LPNB ###
    app.add_css_file("css/common.css")  ### by LPNB ###
    app.add_css_file("css/lpn.css")  ### by LPNB ###
    app.add_js_file("js/lpnb.js")  ### by LPNB ###
