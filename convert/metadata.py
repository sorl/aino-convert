import pyexiv2
from django.utils.translation import get_language
from convert.conf import settings


XMP_DC_PROPERTIES = (
    'contributor',
    'coverage',
    'creator',
    'date',
    'description',
    'format',
    'identifier',
    'language',
    'publisher',
    'relation',
    'rights',
    'source',
    'subject',
    'title',
    'type',
)

XMP_DC_LANGALT_PROPERTIES = (
    'description',
    'rights',
    'title',
)

XMP_DC_BAGSEQ_PROPERTIES = (
    'contributor',
    'creator',
    'language',
    'publisher',
    'relation',
    'subject',
    'type',
)


class MetadataAttributeError(Exception):
    def __init__(self, name, *args, **kwargs):
        super(MetadataAttributeError, self).__init__(
                '`%s` is not a valid XMP.dc property.' % name, *args, **kwargs)


class Metadata(object):
    """
    pyexiv2 XMP.dc metadata proxy
    """

    # TODO make methods to access bags and sequences properly

    def __init__(self, path, lang=None):
        self._lang = lang or get_language()
        self._metadata = pyexiv2.ImageMetadata(path)
        self._metadata.read()

    def __getattr__(self, name):
        if name not in XMP_DC_PROPERTIES:
            raise MetadataAttributeError(name)
        try:
            value = self._metadata['Xmp.dc.%s' % name].value
        except KeyError:
            return None
        if name in XMP_DC_LANGALT_PROPERTIES:
            try:
                value = value[self._lang]
            except KeyError:
                try:
                    value = value['x-default']
                except KeyError:
                    value = ''
        elif name in XMP_DC_BAGSEQ_PROPERTIES:
            value = ', '.join(value)
        return value

    def __setattr__(self, name, value):
        if name.startswith('_'):
            object.__setattr__(self, name, value)
        elif name in XMP_DC_PROPERTIES:
            if name in XMP_DC_LANGALT_PROPERTIES:
                try:
                    obj = self._metadata['Xmp.dc.%s' % name].value
                except KeyError:
                    obj = {}
                obj[self._lang] = value
                value = obj
            elif name in XMP_DC_BAGSEQ_PROPERTIES:
                if not isinstance(value, (tuple, list)):
                    value = [value]
            self._metadata['Xmp.dc.%s' % name] = value
        else:
            raise MetadataAttributeError(name)

    def write(self, obj=None):
        if obj is not None:
            for k, v in obj.items():
                if k not in XMP_DC_PROPERTIES:
                    raise MetadataAttributeError(k)
                setattr(self, k, v)
        try:
            self._metadata.write()
        except ValueError:
            if settings.CONVERT_METADATA_DEBUG:
                raise

