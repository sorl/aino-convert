from os.path import abspath, dirname, join as pjoin
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


fn = abspath(pjoin(dirname(__file__), 'README.rst'))
fp = open(fn, 'r')
long_description = fp.read()
fp.close()

setup(
    name='aino-convert',
    version='0.1.0.10',
    url='http://bitbucket.org/aino/aino-convert/',
    license='BSD',
    author='Mikko Hellsing',
    author_email='mikko@aino.se',
    description='Magick for Django',
    long_description=long_description,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Multimedia :: Graphics',
        'Framework :: Django',
    ],
    packages=[
        'convert',
        'convert.conf',
        'convert.templatetags',
    ],
    platforms='any'
)
