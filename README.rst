aino-convert
============

aino-convert is a basically wrapper for `ImageMagick convert`_ with caching.
The main purpose is to help generate quality thumbnails simply and
efficiently. During the development of sorl-thumbnail I learned some and
eventually I took the plunge to write something using ImageMagick convert
instead of PIL.

Pros
----
- Simple thumbnail tag generating high quality output
- Remote files handling on the fly
- Usage of convert commandline syntax for infinate flexibility
- Caching mechanism
- Cleanup of unused images or conversions of images can be made
- Storage is local file storage only

Cons
----
- Requirements: convert, pyexiv2 is nice to have
- Storage is local file storage only
- Security (protecting the developer from himself)

Demo
====
There is a demo in the `demo` directory.
To run the demo it just cd in to it and type: `./run`


.. _ImageMagic convert: http://www.imagemagick.org/
