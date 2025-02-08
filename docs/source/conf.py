# Configuration file for the Sphinx documentation builder.

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
    'sphinx_jinja2',
]

intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
    'sphinx': ('https://www.sphinx-doc.org/en/master/', None),
}
intersphinx_disabled_domains = ['std']

latex_engine = 'xelatex'

latex_elements = {
    'preamble': r'''
    \usepackage{fontspec}
    \usepackage{xeCJK}  # 支持中文和日文
    \setCJKmainfont{IPAexMincho}  # 设置日文字体为 IPAexMincho
    \setmainfont{Times New Roman}  # 设置英文字体
    '''
}

templates_path = ['_templates']

source_suffix = ['.rst', '.md']

master_doc = 'index'

# -- Options for HTML output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
html_logo = '_static/images/logo.png'
html_favicon = '_static/images/favicon.png'
html_title = "WCC Contact Center Documentation | Best Multi-Channel Call Center Software & Auto Dialer"
html_description = "WCC contact center system is a cloud native solution, and also has an intelligent contact center architecture and solutions which is designed for the growing needs of multichannel customers in order to deliver an intelligent and efficient operational experience for you."
html_keywords = "WCC contact center, cloud-native solution, intelligent contact center, multichannel customers, operational efficiency, AI-driven contact center, omnichannel support, VoIP, IP PBX, Best Call Center Software, Auto Dialer"

# -- Options for EPUB output
epub_show_urls = 'footnote'

gettext_uuid = True
locale_dirs = ['locales/']
