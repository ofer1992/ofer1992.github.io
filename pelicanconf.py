AUTHOR = 'Ofer Yehuda'
SITENAME = 'The Title'
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
LINKS = (('Pelican', 'https://getpelican.com/'))

# Social widget
SOCIAL = (('github', 'https://github.com/ofer1992'))

PLUGINS = ['pelican.plugins.render_math']

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True