# Configuration file for the Sphinx documentation builder.
import os

# -- Project information

project = 'WCC Documentation'
copyright = '%Y Sonicwell Technology Ltd'
author = 'The Sonicwell Team'

release = '0.1'
version = '0.1.0'

# -- General configuration

extensions = [
    'sphinx.ext.duration',
    'sphinx.ext.doctest',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.intersphinx',
    'myst_parser',
]

intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
    'sphinx': ('https://www.sphinx-doc.org/en/master/', None),
}
intersphinx_disabled_domains = ['std']

language = os.getenv('language', 'en')
if language == 'zh_CN':
    latex_engine = 'xelatex'
elif language == 'ja':
    latex_engine = 'uplatex'
else:
    latex_engine = 'pdflatex'

latex_elements = {
    'preamble': r'''
    \usepackage{fontspec}
    \usepackage{xeCJK}
    \setCJKmainfont{Noto Serif CJK SC}
    \setCJKsansfont{Noto Sans CJK SC}
    \setCJKmonofont{Noto Sans Mono CJK SC}
    \setmainfont{Liberation Serif}
    \setCJKfamilyfont{mj}{Noto Sans CJK JP}
    \setCJKfallbackfamilyfont{\CJKrm}{Noto Sans CJK SC}
    \setCJKfallbackfamilyfont{\CJKsf}{Noto Serif CJK JP}
    \setCJKfallbackfamilyfont{\CJKtt}{Noto Sans Mono CJK SC}
    '''
}
latex_show_urls = 'footnote'
latex_use_xindy = True

templates_path = ['_templates']

source_suffix = ['.rst', '.md']

master_doc = 'index'

# -- Options for HTML output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
html_logo = '_static/images/logo.png'
html_favicon = '_static/images/favicon.png'

# -- Options for EPUB output
epub_show_urls = 'footnote'

gettext_uuid = True
locale_dirs = ['locales/']
