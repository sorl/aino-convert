from __future__ import with_statement
import os
import random
import re
import hashlib
from os.path import isfile, isdir, getmtime, dirname, getsize, normpath, join as pjoin
from PIL import Image
from django.utils._os import safe_join
from django.utils.encoding import force_unicode, smart_str, iri_to_uri
from django.utils.safestring import mark_safe
from convert import helpers
from convert.conf import settings


re_remote = re.compile(r'^(https?|ftp):\/\/')
re_whitespace = re.compile('\s{2,}')


class MediaFile(object):
    """
    A media file wrapper, targeted for image manipulation using
    ImageMagick convert.
    """
    def __init__(self, name):
        name = force_unicode(name)
        # remote files need to be cached first
        if re_remote.match(name):
            ext = os.path.splitext(name)[1].strip('.')
            cached = get_mediafile(name, ext)
            if not cached.exists():
                try:
                    helpers.execute(settings.CONVERT_WGET_PATH,
                        ['-T', '%s' % settings.CONVERT_REMOTE_TIMEOUT,
                        '-O', cached.path, name])
                except helpers.ExecuteException:
                    # we treat this as source missing
                    pass
                else:
                    cached.set_xmp({'source': name})
            name = cached.name
        self.name = name
        path = normpath(safe_join(settings.MEDIA_ROOT, self.name))
        self.path = smart_str(path)
        path_dir = dirname(self.path)
        if not isdir(path_dir):
            os.makedirs(path_dir)

    def __unicode__(self):
        return self.name

    def _get_dimensions(self):
        if not hasattr(self, '_dimensions'):
            self._dimensions = Image.open(self.path).size
        return self._dimensions
    dimensions = property(_get_dimensions)
    
    width = property(lambda self: self.dimensions[0])
    height = property(lambda self: self.dimensions[1])

    def size(self):
        return getsize(self.path)

    def _get_tag(self):
        return settings.CONVERT_TAG % {
            'width': self.width,
            'height': self.height,
            'url': self.url,
        } 
    tag = property(_get_tag)

    def _get_relative_url(self):
        return iri_to_uri(self.name.replace('\\', '/'))
    relative_url = property(_get_relative_url)
    
    def _get_url(self):
        if not hasattr(self, '_url'):
            random.seed(self.name)
            base_url = random.choice(settings.STATIC_URLS)
            random.seed() # reset the seed
            self._url = "%s%s" % (base_url, self.relative_url)
        return self._url
    url = property(_get_url)

    def set_xmp(self, params, clear=True):
        if settings.CONVERT_SET_XMP:
            # some files cannot have XMP metadata written by exiv2, notably GIF
            try:
                helpers.write_xmp(self.path, params, clear=clear)
            except helpers.ExecuteException:
                if settings.CONVERT_EXIV2_DEBUG:
                    raise

    def write(self, data):
        with open(self.path, 'wb') as fp:
            fp.write(data)

    def exists(self):
        return isfile(self.path)

    def thumbnail(self, options):
        """
        Simple alternative syntax for thumbnails
        """
        options, ext = helpers.thumbnail_to_convert(options)
        return self.convert(options, ext=ext)

    def convert(self, options, ext=None):
        # we sanitize relation since this is base for the seed and the output
        # filename
        options = re_whitespace.sub(' ', options.strip())
        dest = get_mediafile(options + self.name, ext)
        if not dest.exists() or getmtime(dest.path) < getmtime(self.path):
            args = "%s %s %s" % (self.path, options, dest.path)
            helpers.execute(settings.CONVERT_PATH, args)
            dest.set_xmp({'source': self.name, 'relation': options})
        return dest


class EmptyMediaFile(object):
    """
    Empty instance to be used when CONVERT_DEBUG is False
    """
    url = settings.CONVERT_404_URL
    tag = settings.CONVERT_EMPTY_TAG

    def __unicode__(self):
        return ''

    def __getattr__(self, name):
        return ''


def get_mediafile(seed, ext=None):
    """
    Function to get MediaFile instance based on seed and ext
    """
    hash_ = hashlib.md5(smart_str(seed)).hexdigest()
    ext = ext or settings.CONVERT_EXTENSION
    sub_tree = os.sep.join([hash_[n:n + 2] for n in xrange(0,
            settings.CONVERT_CACHE_SUBDIR_LEVELS * 2, 2)])
    name = pjoin(settings.CONVERT_CACHE, sub_tree, "%s.%s" % (hash_, ext))
    return MediaFile(name)

def convert_solo(options, ext=None):
    options = re_whitespace.sub(' ', options.strip())
    dest = get_mediafile(options, ext)
    if not dest.exists():
        args = "%s %s" % (options, dest.path)
        helpers.execute(settings.CONVERT_PATH, args)
        dest.set_xmp({'relation': options})
    return dest
