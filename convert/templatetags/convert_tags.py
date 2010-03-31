from django.template import Library, Node, TemplateSyntaxError
from django.utils.encoding import force_unicode
from convert.base import MediaFile, EmptyMediaFile, convert_solo
from convert.conf import settings


register = Library()


class ConvertBaseNode(Node):
    def error(self, context):
        if settings.CONVERT_DEBUG:
            raise
        elif self.as_var:
            context[self.as_var] = EmptyMediaFile()
            return ''
        return EmptyMediaFile().tag

    def success(self, context, dest):
        if self.as_var:
            context[self.as_var] = dest
            return ''
        return dest.tag


class ThumbnailNode(ConvertBaseNode):
    def __init__(self, input_file, options, as_var):
        self.input_file = input_file
        self.options = options
        self.as_var = as_var

    def render(self, context):
        try:
            input_file = force_unicode(self.input_file.resolve(context))
            options = self.options.resolve(context)
            source = MediaFile(input_file)
            dest = source.thumbnail(options)
        except:
            return self.error(context)
        return self.success(context, dest)


class ConvertNode(ConvertBaseNode):
    def __init__(self, input_file, options, ext,
            as_var):
        self.input_file = input_file
        self.options = options
        self.ext = ext
        self.as_var = as_var

    def render(self, context):
        try:
            input_file = force_unicode(self.input_file.resolve(context))
            options = self.options.resolve(context)
            ext = self.ext and self.ext.resolve(context)
            if not input_file:
                dest = convert_solo(options, ext)
            else:
                source = MediaFile(input_file)
                dest = source.convert(options, ext)
        except:
            return self.error(context)
        return self.success(context, dest)


@register.tag
def thumbnail(parser, token):
    args = token.split_contents()
    invalid_syntax = TemplateSyntaxError('Invalid syntax.\nGot: %s\n'
            'Expected: thumbnail "input-file" "options" [as var]'
            % " ".join(args))
    as_var = None
    if len(args) not in (3, 5):
        raise invalid_syntax
    if args[-2] == 'as':
        as_var = args[-1]
        args = args[:-2]
    if len(args) != 3:
        raise invalid_syntax
    input_file, options = map(parser.compile_filter, args[1:])
    return ThumbnailNode(input_file, options, as_var)

@register.tag
def convert(parser, token):
    args = token.split_contents()
    invalid_syntax = TemplateSyntaxError('Invalid syntax.\nGot: %s.\n'
            'Expected: convert "input-file" "options" ["extension"] '
            '[as var]' % " ".join(args))
    as_var = None
    ext = None
    if len(args) < 3:
        raise invalid_syntax
    if args[-2] == 'as':
        as_var = args[-1]
        args = args[:-2]
    if len(args) == 4:
        ext = parser.compile_filter(args.pop(3))
    if len(args) != 3:
        raise invalid_syntax
    input_file, options = map(parser.compile_filter,
            args[1:])
    return ConvertNode(input_file, options, ext, as_var)

