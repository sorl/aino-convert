from __future__ import with_statement
import hashlib
import os
import random
import re
import socket
import urllib2
from os.path import isfile, isdir, getmtime, dirname, getsize, normpath, join as pjoin
from PIL import Image
from django.utils.encoding import force_unicode, smart_str, iri_to_uri
from django.utils._os import safe_join
from django.utils.safestring import mark_safe
from convert import helpers
from convert.conf import settings


re_remote = re.compile(r'^(https?|ftp):\/\/')
re_whitespace = re.compile(r'\s{2,}')
re_ext = re.compile(r'\.([a-zA-Z]{2,4})$')



class MediaFile(object):
    """
    A media file wrapper, targeted for image manipulation using
    ImageMagick convert.
    """
    def __init__(self, name):
        name = force_unicode(name)
        # remote files need to be local first
        if re_remote.match(name):
            name = get_remote(name).name
        self.name = name
        self.path = normpath(safe_join(settings.MEDIA_ROOT, self.name))
        path_dir = dirname(self.path)
        if not isdir(path_dir):
            os.makedirs(path_dir)

    def __unicode__(self):
        return self.name

    def __len__(self):
        "This is for field validation"
        return len(self.name)

    @property
    def dimensions(self):
        if not hasattr(self, '_dimensions'):
            try:
                self._dimensions = Image.open(self.path).size
            except:
                if settings.CONVERT_DEBUG:
                    raise
                else:
                    self._dimensions = ('', '')
        return self._dimensions

    width = property(lambda self: self.dimensions[0])
    height = property(lambda self: self.dimensions[1])

    @property
    def size(self):
        return getsize(self.path)

    @property
    def tag(self):
        return mark_safe(settings.CONVERT_TAG % {
            'width': self.width,
            'height': self.height,
            'url': self.url,
        })

    @property
    def relative_url(self):
        return iri_to_uri(self.name.replace('\\', '/'))

    @property
    def url(self):
        if not hasattr(self, '_url'):
            random.seed(self.name)
            base_url = random.choice(settings.STATIC_URLS)
            random.seed() # reset the seed
            self._url = "%s%s" % (base_url, self.relative_url)
        return self._url

    #TODO: cache alternatives for "expensive" disk operations like this
    @property
    def metadata(self):
        if not hasattr(self, '_metadata'):
            try:
                from metadata import Metadata
            except ImportError:
                self._metadata = None
            else:
                self._metadata = Metadata(self.path)
        return self._metadata

    def _write_metadata(self, obj):
        if settings.CONVERT_WRITE_METADATA:
            self.metadata.write(obj)

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
        options = "%s %s %s" % (settings.CONVERT_PREPEND, options,
                settings.CONVERT_APPEND)
        options = re_whitespace.sub(' ', options.strip())
        dest = get_mediafile(options + self.name, ext)
        if not dest.exists() or getmtime(dest.path) < getmtime(self.path):
            args = "%s %s %s" % (self.path, options, dest.path)
            helpers.execute(settings.CONVERT_PATH, args)
            dest._write_metadata({'source': self.name, 'relation': [options]})
        return dest


class EmptyMediaFile(object):
    """
    Empty instance to be used when CONVERT_DEBUG is False
    """
    url = settings.CONVERT_404_URL
    tag = settings.CONVERT_EMPTY_TAG

    def __unicode__(self):
        return ''

    def __len__(self):
        return 0

    def __getattr__(self, name):
        return ''


def get_remote(name):
    """
    Gets a remote file and stores locally
    """
    # we can only use the filename to guess extension
    m = re_ext.search(name)
    ext = m and m.group(1).lower() or 'jpg' # brutally resort to jpg
    cached = get_mediafile(name, ext)
    if not cached.exists():
        # this is the only timeout option for urllib2 in python <= 2.5.x
        socket.setdefaulttimeout(settings.CONVERT_REMOTE_TIMEOUT)
        try:
            data = urllib2.urlopen(name).read()
        except:
            return cached
        cached.write(data)
        cached._write_metadata({'source': name})
    return cached

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
        dest._write_metadata({'relation': [options]})
    return dest

