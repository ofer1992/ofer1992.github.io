AUTHOR = 'Ofer Yehuda'
SITENAME = 'Integrably Sorry'
SITEURL = ''

PATH = 'content'

TIMEZONE = 'Asia/Jerusalem'

DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
# LINKS = (('Pelican', 'https://getpelican.com/'),
#          ('Python.org', 'https://www.python.org/'),
#          ('Jinja2', 'https://palletsprojects.com/p/jinja/'),
#          ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (('github', 'https://github.com/ofer1992'), ('twitter', 'https://x.com/oferyehuda'))

PLUGINS = ['pelican.plugins.render_math']

MARKDOWN = {
    'extensions': [
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'obsidian_markdown',
    ],
    'extension_configs': {
        'markdown.extensions.codehilite': {
            'css_class': 'highlight',
            'guess_lang': False,
        },
        'obsidian_markdown': {
            'content_root': PATH,
            'static_dirs': ['images', 'audio'],
        },
    },
    'output_format': 'html5',
}

STATIC_PATHS = ['images', 'audio', 'extra']

# Map extra files to their output locations
EXTRA_PATH_METADATA = {
    'extra/ansi-colors.css': {'path': 'theme/css/ansi-colors.css'},
    'extra/custom.css': {'path': 'theme/css/custom.css'}
}

# Use custom CSS file that imports main theme + ANSI colors
CSS_FILE = 'custom.css'

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
