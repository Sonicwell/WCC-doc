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
    'sphinx.ext.ifconfig',
    'sphinx.ext.viewcode',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.intersphinx',
    'sphinx.ext.imgconverter',
    'sphinx.ext.todo',
    'sphinx.ext.imgmath',
    'myst_parser',
]

intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
    'sphinx': ('https://www.sphinx-doc.org/en/master/', None),
}
intersphinx_disabled_domains = ['std']

latex_engine = 'xelatex'

latex_elements = {
    'preamble': r'''
    \usepackage{graphicx}
    \usepackage{grffile}  # 允许复杂图片路径
    \DeclareGraphicsExtensions{.pdf,.png,.jpg,.jpeg}

    \usepackage[UTF8]{ctex}  # 中文支持
    \setCJKmainfont{WenQuanYi Zen Hei}  # 设置中文字体
    \setCJKmonofont{WenQuanYi Zen Hei Mono}  # 设置中文等宽字体

    \usepackage{xeCJK}  # 日文支持
    \setCJKfamilyfont{jp}{IPAexMincho}  # 设置日文字体
    \newcommand{\jp}[1]{{\CJKfamily{jp}#1}}  # 定义日文命令
    ''',
    'figure_align': 'H',
}

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

