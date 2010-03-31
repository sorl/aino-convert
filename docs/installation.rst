============
Installation
============

Requirements
============

Python
------
You will need at least Python 2.5. We are currently running against 2.6.
There are no plans to make this compatible with anything lower than 2.5.

`Python Imaging Library`_
-------------------------
Any version should do

`Django`_
---------
Any 1+ version should work

`ImageMagick convert`_
----------------------
If you want to use the thumbnail tag you need a recent version that supports
the ^ modifier for geometrics. Version 6.5.9 tested and works, the version that
comes with Ubuntu 8.04 LTS does not.

`pyexiv2`_
----------
If you want to use the metadata feature you need a recent version of pyexiv2
that supports XMP metadata. We know that pyexiv2 0.2.0 works.


.. _Python Imaging Library: http://www.pythonware.com/products/pil/
.. _Django: http://www.djangoproject.com/download/
.. _ImageMagick convert: http://www.imagemagick.org/script/download.php
.. _pyexiv2: http://tilloy.net/dev/pyexiv2/download.html
