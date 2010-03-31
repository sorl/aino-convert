from django import forms
from django.forms.util import flatatt
from django.utils.safestring import mark_safe
from django.utils.encoding import force_unicode
from base import MediaFile


class AdminMediaFileWidget(forms.TextInput):
    """
    This is just the core of a widget, how it get the actual imput value is
    left to the user, javascript hint.
    """

    def __init__(self, attrs=None):
        final_attrs = {'class': 'mediafile'}
        if attrs is not None:
            final_attrs.update(attrs)
        super(AdminMediaFileWidget, self).__init__(attrs=final_attrs)

    def render(self, name, value, attrs=None):
        if value is None: value = ''
        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        img_tag = ''
        if value != '':
            # Only add the 'value' attribute if a value is non-empty.
            final_attrs['value'] = force_unicode(value)
            img_tag = MediaFile(value).thumbnail('100x100>').tag
        return mark_safe(u'%s<input%s />' % (img_tag, flatatt(final_attrs)))

