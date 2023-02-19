# -*- coding: utf-8 -*-
#
# Zephyr documentation build configuration file.
#
# DERIVE and OVERRIDE AS NEEDED from:
# https://github.com/zephyrproject-rtos/zephyr/raw/zephyr-v2.6.0/doc/conf.py
#
# pylint: skip-file
#

import sys
import os
from pathlib import Path
from sphinx.config import eval_config_file

# Paths ------------------------------------------------------------------------

BRIDLE_BASE = Path(__file__).absolute().parents[2]

# Add the '_extensions' directory to sys.path, to enable finding Bridle's
# utilities for Sphinx configuration within.
sys.path.insert(0, os.path.join(BRIDLE_BASE, 'doc', '_utils'))
import utils

ZEPHYR_BASE = utils.get_projdir('zephyr')
BRIDLE_ZEPHYR_BUILD = os.path.join(utils.get_builddir(), 'zephyr')

# Add the '_extensions' directory to sys.path, to enable finding Bridle's
# Sphinx extensions within.
sys.path.insert(0, os.path.join(BRIDLE_BASE, 'doc', '_extensions'))

# Import all Zephyr configuration, override as needed later
conf = eval_config_file(os.path.join(ZEPHYR_BASE, 'doc', 'conf.py'), tags)
locals().update(conf)

# pylint: disable=undefined-variable

# Project ----------------------------------------------------------------------

# General information about the project.
project = utils.get_projname('zephyr')

# The following code tries to extract the information by reading the Makefile,
# when Sphinx is run directly (e.g. by Read the Docs).
try:
    bridle_version_major = None
    bridle_version_minor = None
    bridle_patchlevel = None
    bridle_extraversion = None
    for line in open(os.path.join(BRIDLE_BASE, 'VERSION')):
        key, val = [x.strip() for x in line.split('=', 2)]
        if key == 'VERSION_MAJOR':
            bridle_version_major = val
        if key == 'VERSION_MINOR':
            bridle_version_minor = val
        elif key == 'PATCHLEVEL':
            bridle_patchlevel = val
        elif key == 'EXTRAVERSION':
            bridle_extraversion = val
        if (
            bridle_version_major
            and bridle_version_minor
            and bridle_patchlevel
            and bridle_extraversion
        ):
            break
except Exception:
    pass
finally:
    if (
        bridle_version_major
        and bridle_version_minor
        and bridle_patchlevel
        and bridle_extraversion
        is not None
    ):
        bridle_version = bridle_release                 \
                       = bridle_version_major           \
                       + '.' + bridle_version_minor     \
                       + '.' + bridle_patchlevel
        if bridle_extraversion != '':
            bridle_version = bridle_release             \
                           = bridle_version             \
                           + '-' + bridle_extraversion
    else:
        sys.exit('Could not extract Bridle version.')

# General ----------------------------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
needs_sphinx = '4.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones. Extensions that interfere should also removed here.
extensions.extend([
    'sphinx.ext.intersphinx',
    'bridle.inventory_builder',
])
extensions.remove('zephyr.vcs_link')

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

# Options for zephyr.doxyrunner plugin -----------------------------------------

doxyrunner_doxygen = os.environ.get('DOXYGEN_EXECUTABLE', 'doxygen')
doxyrunner_doxydir = os.environ.get('DOCSET_DOXY_PRJ', os.path.join(
                      ZEPHYR_BASE, 'doc', '_doxygen'))
doxyrunner_doxyfile = os.environ.get('DOCSET_DOXY_IN', os.path.join(
                      BRIDLE_BASE, 'doc', '_doxygen', 'doxyfile-zephyr.in'))
doxyrunner_outdir = os.path.join(ZEPHYR_BUILD, 'doxygen')
doxyrunner_outdir_var = 'DOXY_OUT'
doxyrunner_silent = True
doxyrunner_fmt = True
doxyrunner_fmt_pattern = '@{}@'
doxyrunner_fmt_vars = {
    'DOXY_SET': u'zephyr',
    'DOXY_IN': str(Path(doxyrunner_doxyfile).absolute().parent),
    'PROJECT_DOXY': str(Path(doxyrunner_doxydir).absolute()),
    'PROJECT_BASE': str(ZEPHYR_BASE),
    'PROJECT_NAME': project,
    'PROJECT_VERSION': version,
    'PROJECT_BRIEF': str(os.environ.get('DOCSET_BRIEF', 'Unknown project brief!')),
}

# Options for zephyr.warnings_filter -------------------------------------------

warnings_filter_config = os.path.join(BRIDLE_ZEPHYR_BUILD, 'known-warnings.txt')
warnings_filter_silent = False

# -- Options for notfound.extension --------------------------------------------

notfound_urls_prefix = '/doc/{}/zephyr/'.format(
    bridle_version if is_release else 'latest'
)

# Options for zephyr.external_content ------------------------------------------

# Clear external content keeping, Bridle provides its own docsets for that.
external_content_keep.clear()

# pylint: enable=undefined-variable,used-before-assignment


def setup(app):
    app.add_css_file('css/common.css')
    app.add_css_file('css/zephyr.css')
