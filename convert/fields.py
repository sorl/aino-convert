from django.core.exceptions import ValidationError
from django.db import models
from django.utils.encoding import force_unicode
from base import MediaFile


class MediaFileField(models.CharField):
    """
    The main idea is to have a filepath relative MEDIA_ROOT in this field. It
    is up to the user to implement how this is acheived. It does by design not
    delete or handle files in any other way than to instantiate a MediaFile
    class with the db value.
    """

    __metaclass__ = models.SubfieldBase

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = kwargs.get('max_length', 200)
        super(MediaFileField, self).__init__(*args, **kwargs)

    def get_internal_type(self):
        return 'CharField'

    def get_prep_value(self, value):
        """
        MediaFile instance returns MEDIA_ROOT relative path in __unicode__
        """
        if not value:
            return value
        return force_unicode(value)

    def to_python(self, value):
        if not value:
            return value
        try:
            return MediaFile(value)
        except Exception, e:
            raise ValidationError(e.message)

