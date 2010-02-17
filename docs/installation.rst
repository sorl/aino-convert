============
Installation
============

Requirements
============

Python
------
You will need at least Python 2.5, no other versions tested at the moment.
There are no plans to make this compatible with anything lower than 2.5.

`Python Imaging Library`_
-------------------------
Any version should do

`Django`_
---------
Any 1+ version should work

`ImageMagick convert`
---------------------
If you want to use the thumbnail tag you need a recent version that supports
the ^ modifier for geometrics. Version 6.5.9 tested and works, the version that
comes with Ubuntu 8.04 LTS does not.

`Exiv2`
-------
If you want to use the XMP feature you need a recent version of Exiv2 that
supports XMP metadata. Version 0.19 tested and works, the version that comes
with Ubuntu 8.04 LTS does not.

wget
----
To be ably to download external sources on the fly you need wget.

.. _Python Imaging Library: http://www.pythonware.com/products/pil/
.. _Django: http://www.djangoproject.com/download/
.. _ImageMagick convert: http://www.imagemagick.org/script/download.php
.. _Exiv2: http://www.exiv2.org/download.html
