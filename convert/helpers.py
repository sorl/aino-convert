import re
from subprocess import Popen, PIPE
from convert.conf import settings
from django.utils.encoding import smart_str, DEFAULT_LOCALE_ENCODING


re_geometry = re.compile('^(\d+)[\^><]*x(\d+)[\^><]*$')
re_width = re.compile('^(\d+)[\^><]*$')
re_height = re.compile('^x(\d+)[\^><]*$')


class ThumbnailException(Exception):
    pass

class ExecuteException(Exception):
    pass


def execute(cmd, args):
    """
    Just a simple wrapper for executing commands. args is expected to be a
    sequence or a basestring, a basestring will be executed with shell=True.
    """
    if isinstance(args, basestring):
        args = '%s %s' % (cmd, args)
        args = smart_str(args)
        shell = True
    else:
        args.insert(0, cmd)
        args = map(smart_str, args)
        shell = False
    p = Popen(args, shell=shell, stderr=PIPE, stdout=PIPE)
    retcode = p.wait()
    if retcode != 0:
        raise ExecuteException(p.stderr.read().decode(DEFAULT_LOCALE_ENCODING))
    return p.stdout.read().decode(DEFAULT_LOCALE_ENCODING)

def thumbnail_to_convert(value):
    """
    Helper function to generate proper convert args syntax from a simpler
    syntax. returns convert output-options
    """
    if not len(value):
        raise ThumbnailException('Missing argument.')
    input_args = value.split(',')
    geometry = input_args.pop(0)
    # < and > mess up highlighting in html editors
    geometry = geometry.replace('gt', '>').replace('lt', '<')
    kwargs = {}
    for arg in input_args:
        arg = arg.strip().split('=')
        kwargs[arg[0]] = arg[1] if len(arg) > 1 else None

    def get_dimensions():
        m = re_geometry.match(geometry)
        if m:
            return m.groups()
        m = re_width.match(geometry)
        if m:
            return m.group(1), None
        m = re_height.match(geometry)
        if m:
            return None, m.group(1)
        return None

    dimensions = get_dimensions()
    if dimensions is None:
        raise ThumbnailException('Invalid geometry.')

    # We don't strip the resulting thumbnail, since we want to keep metadata
    # that we might have set on the source file
    args = ["-resize '%s'" % geometry]
    if 'crop' in kwargs:
        if None in dimensions:
            raise ThumbnailException('crop needs both width and height.')
        args.insert(0, '-gravity center')
        args.append('-crop %sx%s+0+0' % dimensions)
    if kwargs.get('colorspace'):
        args.append('-colorspace %s' % kwargs['colorspace'])
    if kwargs.get('sharpen'):
        args.append('-sharpen %s' % kwargs['sharpen'])
    quality = kwargs.get('quality', settings.CONVERT_THUMBNAIL_QUALITY)
    args.append('-quality %s' % quality)
    return " ".join(args), kwargs.get('ext')

