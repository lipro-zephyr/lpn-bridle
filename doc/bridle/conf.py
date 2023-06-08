# -*- coding: utf-8 -*-
#
# Bridle documentation build configuration file.
#
# COPIED and CHANGED from:
# https://github.com/zephyrproject-rtos/zephyr/raw/zephyr-v2.6.0/doc/conf.py
#
# pylint: skip-file
#

import sys
import os
from pathlib import Path

from sphinx.cmd.build import get_parser

# Paths ------------------------------------------------------------------------

args = get_parser().parse_args()
BRIDLE_BASE = Path(__file__).absolute().parents[2]
BRIDLE_BUILD = Path(args.outputdir).resolve()

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
project = utils.get_projname('bridle')
copyright = u'2019-2022 TiaC Systems members and individual contributors'
author = u'TiaC Systems'

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

# General ----------------------------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
needs_sphinx = '5.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'breathe',
    'interbreathe',
#   'table_from_rows',
    'tsn_include',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx.ext.extlinks',
#   'sphinx.ext.autodoc',
    'sphinx.ext.graphviz',
    'sphinx.ext.ifconfig',
    'sphinxcontrib.mscgen',
    'sphinx_tabs.tabs',
    'crate.sphinx.csv',
    'zephyr.application',
    'zephyr.html_redirects',
    'zephyr.kconfig',
    'zephyr.dtcompatible-role',
    'zephyr.link-roles',
    'zephyr.warnings_filter',
    'zephyr.doxyrunner',
#   'zephyr.vcs_link',
    'zephyr.external_content',
    'sphinx_copybutton',
    'notfound.extension',
    'bridle.link-roles',
    'bridle.inventory_builder',
    'bridle.options_from_kconfig',
    'bridle.manifest_revisions_table',
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

rst_prolog = '''
.. include:: /roles.txt
'''

rst_epilog = '''
.. include:: /links.txt
.. include:: /shortcuts.txt
.. include:: /versions.txt
'''

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
    'docsets': utils.get_docsets('bridle'),
    'default_docset': utils.get_default_docset(),
}

# Options for intersphinx ------------------------------------------------------

intersphinx_mapping = dict()

zephyr_mapping = utils.get_intersphinx_mapping('zephyr')
if zephyr_mapping:
    intersphinx_mapping['zephyr'] = zephyr_mapping

kconfig_mapping = utils.get_intersphinx_mapping('kconfig')
if kconfig_mapping:
    intersphinx_mapping['kconfig'] = kconfig_mapping

devicetree_mapping = utils.get_intersphinx_mapping('devicetree')
if devicetree_mapping:
    intersphinx_mapping['devicetree'] = devicetree_mapping

# Options for zephyr.doxyrunner plugin -----------------------------------------

doxyrunner_doxygen = os.environ.get('DOXYGEN_EXECUTABLE', 'doxygen')
doxyrunner_doxydir = os.environ.get('DOCSET_DOXY_PRJ', os.path.join(
                      BRIDLE_BASE, 'doc', '_doxygen'))
doxyrunner_doxyfile = os.environ.get('DOCSET_DOXY_IN', os.path.join(
                      BRIDLE_BASE, 'doc', '_doxygen', 'doxyfile-bridle.in'))
doxyrunner_outdir = os.path.join(BRIDLE_BUILD, 'doxygen')
doxyrunner_outdir_var = 'DOXY_OUT'
doxyrunner_silent = True
doxyrunner_fmt = True
doxyrunner_fmt_pattern = '@{}@'
doxyrunner_fmt_vars = {
    'DOXY_SET': u'bridle',
    'DOXY_IN': str(Path(doxyrunner_doxyfile).absolute().parent),
    'DOXY_LAYOUT': u'zephyr-doxyrunner',
    'PROJECT_DOXY': str(Path(doxyrunner_doxydir).absolute()),
    'PROJECT_BASE': str(BRIDLE_BASE),
    'PROJECT_NAME': project,
    'PROJECT_VERSION': version,
    'PROJECT_BRIEF': str(os.environ.get('DOCSET_BRIEF', 'Unknown project brief!')),
}

# Options for breathe ----------------------------------------------------------

breathe_projects = {project: '{}/xml'.format(doxyrunner_outdir)}
breathe_default_project = project
breathe_domain_by_extension = {
    'h': 'c',
    'c': 'c',
}
breathe_show_enumvalue_initializer = True
breathe_separate_member_pages = True

cpp_id_attributes = [
    '__syscall',
    '__deprecated',
    '__may_alias',
    '__used',
    '__unused',
    '__weak',
    '__attribute_const__',
    '__DEPRECATED_MACRO',
    'FUNC_NORETURN',
    '__subsystem',
    'ALWAYS_INLINE',
]
c_id_attributes = cpp_id_attributes

# Options for tsn_include ------------------------------------------------------

tsn_include_mapping = {
    'zephyr': utils.get_srcdir('zephyr'),
    'kconfig': utils.get_srcdir('kconfig'),
    'devicetree': utils.get_srcdir('devicetree'),
    'bridle': utils.get_srcdir('bridle'),
}

# Options for zephyr.warnings_filter -------------------------------------------

warnings_filter_config = os.path.join(BRIDLE_BASE, 'doc', 'bridle', 'known-warnings.txt')
warnings_filter_silent = False

# -- Options for notfound.extension --------------------------------------------

notfound_urls_prefix = '/doc/{}/bridle/'.format(
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
    (BRIDLE_BASE / 'doc' / 'bridle', '[!_]*'),
    (BRIDLE_BASE, 'boards/**/*.rst'),
    (BRIDLE_BASE, 'boards/**/doc'),
    (BRIDLE_BASE, 'samples/**/*.rst'),
    (BRIDLE_BASE, 'samples/**/doc'),
    (BRIDLE_BASE, 'applications/**/*.rst'),
    (BRIDLE_BASE, 'applications/**/doc'),
    (BRIDLE_BASE, 'drivers/**/*.rst'),
    (BRIDLE_BASE, 'drivers/**/doc'),
    (BRIDLE_BASE, 'subsys/**/*.rst'),
    (BRIDLE_BASE, 'subsys/**/doc'),
    (BRIDLE_BASE, 'lib/**/*.rst'),
    (BRIDLE_BASE, 'lib/**/doc'),
    (BRIDLE_BASE, 'include/**/*.rst'),
    (BRIDLE_BASE, 'scripts/**/*.rst'),
    (BRIDLE_BASE, 'tests/**/*.rst'),
]
external_content_keep = ['versions.txt']

# Options for bridle.options_from_kconfig --------------------------------------

options_from_kconfig_base_dir = BRIDLE_BASE
options_from_kconfig_zephyr_dir = ZEPHYR_BASE

# Options for bridle.manifest_revisions_table ----------------------------------

manifest_revisions_table_manifest = os.path.join(BRIDLE_BASE, 'west.yml')

# -- Options for sphinx.ext.graphviz --------------------------------------

graphviz_dot = os.environ.get('DOT_EXECUTABLE', 'dot')
graphviz_output_format = 'svg'
graphviz_dot_args = [
    '-Gbgcolor=transparent',
    '-Nstyle=filled',
    '-Nfillcolor=white',
    '-Ncolor=gray60',
    '-Nfontcolor=gray25',
    '-Ecolor=gray60',
]

# Linkcheck options ------------------------------------------------------------

extlinks = {
    'github': ('https://github.com/tiacsys/bridle/issues/%s', 'GitHub #%s'),
}

linkcheck_ignore = [
    # intersphinx links
    r'(\.\.(\\|/))+(zephyr|kconfig|devicetree)',
    # redirecting and used in release notes
    'https://github.com/tiacsys/bridle',
    # link to access local documentation
    'http://localhost:4711/latest/index.html',
    'http://localhost:8000/latest/index.html',
    'http://localhost:8080/latest/index.html',
]

linkcheck_timeout = 30
linkcheck_workers = 10
linkcheck_anchors = True
linkcheck_anchors_ignore = [r'page=']


def setup(app):
    app.add_css_file('css/common.css')
    app.add_css_file('css/bridle.css')
    app.add_css_file('css/colors.css')
    app.add_css_file('css/strikethrough.css')
    app.add_css_file('css/underline.css')
