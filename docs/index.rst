=====
Usage
=====

First of all you need to have the module `convert` in `INSTALLED_APPS`.
In the top of you template first load the `convert` tags, this is done by:
`{% load convert_tags %}`.

There are two tags included: `thumbnail` and `convert`.


thumbnail syntax
----------------
`{% thumbnail input-file options [as var] %}`


input-file
~~~~~~~~~~
This should be either an object resolving to a relative to MEDIA_ROOT
file path or a string with a relative file path or an http(s)/ftp URL
pointing to an image.

options
~~~~~~~
options can be an object resolving to a string or just a string, with
options delimited by comma. The first option must be a geometry specification.
The geometry specification mostly follows that of `ImageMagic geometry`_. Some
modifiers are invalid: `%`, `@`, `!`, some are **valid**: `^`, `>` or `gt`,
`<` or `lt`. General description (actual behavior can vary for different
options and settings):

- `width` Width given, height automagically selected to preserve aspect ratio.

- `xheight` Height given, width automagically selected to preserve aspect
  ratio.

- `widthxheight` Maximum values of height and width given, aspect ratio
  preserved.

- `widthxheight^` Minimum values of width and height given, aspect ratio
  preserved.

- `widthxheight>` Change as per widthxheight but only if an image dimension
  exceeds a specified dimension.

- `widthxheight<` Change dimensions only if both image dimensions exceed
  specified dimensions.


Other valid options:

- `crop` This will crop the image to the specified dimension, note that if you
  really want it to crop as expected be sure to use the `^` modifier.

- `colorspace=value` Set the image colorspace, see `colorspace`_

- `sharpen=radius{xsigma}` Sharpen the image. Use a Gaussian operator of the
  given radius and standard deviation (sigma). `sharpen`_

- `quality=value` JPEG/MIFF/PNG compression level, default is 85. `quality`_

- `ext=value` Extension. The extension will determine the destination format.


as var
~~~~~~
If the next to last argument is `as` then the last last argument is used as
a name for a context variable where to assign the resulting MediaFile class
instance.


convert syntax
---------------
`{% convert input-file options [ext] [as var] %}`

input-file
~~~~~~~~~~
This should be either an object resolving to a relative to MEDIA_ROOT
file path or a string with a relative file path or an http(s)/ftp URL
pointing to an image. Or it can be an empty string if you do not wish to
process an input file at all.

options
~~~~~~~
options can be an object resolving to a string or just a string containing
whatever `ImageMagick output-options`_ you like.

ext
~~~
ext is optional, it can be an object resolving to an extension or an extension
in a string. The extension determines the destination image format.

as var
~~~~~~
If the next to last argument is `as` then the last last argument is used as
a name for a context variable where to assign the resulting MediaFile class
instance.


.. _ImageMagic geometry: http://www.imagemagick.org/script/command-line-processing.php#geometry
.. _ImageMagic options: http://www.imagemagick.org/script/command-line-options.php
.. _colorspace: http://www.imagemagick.org/script/command-line-options.php#colorspace
.. _sharpen: http://www.imagemagick.org/script/command-line-options.php#sharpen
.. _quality: http://www.imagemagick.org/script/command-line-options.php#quality
