from os.path import join as pjoin
from django.conf import settings


# default output extension, you can override this on a per tag basis.
# ImageMagick convert automagically knows the format from extension
CONVERT_EXTENSION = 'jpg'

# default thumbnail quality, 0-100
CONVERT_THUMBNAIL_QUALITY = 85

# prepend all convert commands with this.
CONVERT_PREPEND = '-colorspace RGB'

# appnd all convert commands with the following:
CONVERT_APPEND = ''

# formatting of tag, xhtml anyone?
CONVERT_TAG = '<img width="%(width)s" height="%(height)s" src="%(url)s">'

# spreading media over a few domains can have positive effects on performance
STATIC_URLS = (settings.MEDIA_URL,)

# cache path relative MEDIA_ROOT
CONVERT_CACHE = 'cache'

# number of levels of subdirs to the cache dir, each level will hold 256 dirs.
# Note that if you change this all existing cache will need to be moved or
# re-cached. Comments regardning some values:
# 0: all cached files are storded right under CONVERT_CACHE
# 1: cached files will use 256 sub-directories under CONVERT_CACHE
# 2: CONVERT_CACHE will hold 256 sub-directories each with 256 sub-directories
# 3: will most likely lead to that every cached file will have its own dir
CONVERT_CACHE_SUBDIR_LEVELS = 1

# write XMP metadata to file, this can be useful for finding stale cache
CONVERT_WRITE_METADATA = True

# will be returned on errors rather than an img tag with an empty source which
# is known to cause some serious problems as in requesting the paga aigain
CONVERT_EMPTY_TAG = '<img>'

# url attribute when something goes wrong, use something that returns a 404
CONVERT_404_URL = '/404/'

# path to shell commands, full path is only needed if the command is not in
# users path
CONVERT_PATH = 'convert'

# when True ConvertNode.render can raise errors
CONVERT_DEBUG = False

# when True failing to write XMP metadata can raise errors, note that this
# will always happend when trying to write to files that does not support
# XMP metadata, for example GIF
CONVERT_METADATA_DEBUG = False

# timeout in seconds for caching remote files locally
CONVERT_REMOTE_TIMEOUT = 5

