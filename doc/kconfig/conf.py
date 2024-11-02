# -*- coding: utf-8 -*-
#
# Kconfig reference build configuration file.
#
# COPIED and CHANGED from:
# https://github.com/zephyrproject-rtos/zephyr/raw/zephyr-v2.6.0/doc/conf.py
#
# pylint: skip-file
#

import os
import sys
import sphinx
from pathlib import Path

# Paths ------------------------------------------------------------------------

BRIDLE_BASE = Path(__file__).absolute().parents[2]

# Add the '_extensions' directory to sys.path, to enable finding Bridle's
# utilities for Sphinx configuration within.
sys.path.insert(0, os.path.join(BRIDLE_BASE, 'doc', '_utils'))
import utils

ZEPHYR_BASE = utils.get_projdir('zephyr')

# Add the '_extensions' directory to sys.path, to enable finding Bridle's
# Sphinx extensions within.
sys.path.insert(0, os.path.join(BRIDLE_BASE, 'doc', '_extensions'))

# Add the 'extensions' directory to sys.path, to enable finding Zephyr's
# Sphinx extensions within.
sys.path.insert(0, os.path.join(ZEPHYR_BASE, 'doc', '_extensions'))

# Project ----------------------------------------------------------------------

# General information about the project.
project = utils.get_projname('kconfig')
copyright = u'2015-2024 Zephyr Project and TiaC Systems members and individual contributors'
author = u'The Zephyr Project and TiaC Systems'

# The following code tries to extract the information by reading the Makefile,
# when Sphinx is run directly (e.g. by Read the Docs).
try:
    version_major = None
    version_minor = None
    patchlevel = None
    extraversion = None
    for line in open(os.path.join(BRIDLE_BASE, 'VERSION')):
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
        sys.exit('Could not extract Bridle version.')

# Overview ---------------------------------------------------------------------

logcfg = sphinx.util.logging.getLogger(__name__)
logcfg.info(project + ' ' + release, color='yellow')
logcfg.info('Build with tags: ' + ':'.join(map(str, tags)), color='red')
logcfg.info('BRIDLE_BASE is: "{}"'.format(BRIDLE_BASE), color='green')
logcfg.info('ZEPHYR_BASE is: "{}"'.format(ZEPHYR_BASE), color='green')

# General ----------------------------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
needs_sphinx = '8.1'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx.ext.extlinks',
    'sphinx.ext.ifconfig',
#   'sphinx_tabs.tabs',         # stay in conflict with 'zephyr.kconfig'
    'sphinx_copybutton',
    'notfound.extension',
    'zephyr.dtcompatible-role',
    'zephyr.kconfig',
    'zephyr.external_content',
    'bridle.inventory_builder',
    'bridle.warnings_filter',
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

# The master toctree document.
master_doc = 'index'

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = 'en'

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# If this is True, todo and todolist produce output, else they produce nothing.
# The default is False.
todo_include_todos = False

# Options for HTML output ------------------------------------------------------

# The theme that the HTML output should use.
html_theme = 'sphinx_tsn_theme'

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

html_theme_options = {
    'prev_next_buttons_location': None,
    'docsets': utils.get_docsets('kconfig'),
    'default_docset': utils.get_default_docset(),
}

# Options for intersphinx ------------------------------------------------------

intersphinx_mapping = dict()

zephyr_mapping = utils.get_intersphinx_mapping('zephyr')
if zephyr_mapping:
    intersphinx_mapping['zephyr'] = zephyr_mapping

bridle_mapping = utils.get_intersphinx_mapping('bridle')
if bridle_mapping:
    intersphinx_mapping['bridle'] = bridle_mapping

# -- Options for zephyr.kconfig ------------------------------------------------

kconfig_generate_db = True
kconfig_ext_paths = [ZEPHYR_BASE, BRIDLE_BASE]

# Options for zephyr.warnings_filter -------------------------------------------

warnings_filter_config = os.path.join(BRIDLE_BASE, 'doc', 'kconfig', 'known-warnings.txt')
warnings_filter_silent = True

# -- Options for notfound.extension --------------------------------------------

notfound_urls_prefix = '/doc/{}/kconfig/'.format(
    'latest' if version.endswith('99') else version
)

# Options for zephyr.external_content ------------------------------------------

# Default directives for included content.
external_content_directives = (
    'figure',
    'image',
    'include',
    'literalinclude',
)
external_content_contents = [
    (BRIDLE_BASE / 'doc' / 'kconfig', '[!_]*'),
]
external_content_keep = [
    '**/*.rst',
]


# This function will update the zephyr.warnings_filter setup in case of
# the inventory builder to be more tolerant against missing references.
def update_inventory_warnings_filter_config(app):
    # Check if the value was provided by the original configuration.
    if "warnings_filter_config" in app.config:
        # Update the warnings_filter_config value.
        app.config.warnings_filter_config = os.path.join(
            BRIDLE_BASE, 'doc', 'kconfig', 'known-warnings-inventory.txt'
        )

def update_config(app):
    # Check if a specific builder was initialized by the user.
    if "inventory" == app.builder.name:
        update_inventory_warnings_filter_config(app)

    logcfg.info('Warnings filter from: "{}"'.format(
        app.config.warnings_filter_config
    ), color='yellow')

def setup(app):
    app.connect("builder-inited", update_config, 0)
    app.add_css_file('css/common.css')
    app.add_css_file('css/kconfig.css')
