from os.path import abspath, dirname, join
from setuptools import setup


FOLDER = dirname(abspath(__file__))
DESCRIPTION = '\n\n'.join(open(join(FOLDER, x)).read().strip() for x in [
    'README.rst'])
setup(
    name='crosscompute-types',
    version='0.5.6',
    description='Default data type plugins for CrossCompute',
    long_description=DESCRIPTION,
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Pyramid',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
        'License :: OSI Approved :: MIT License',
    ],
    author='CrossCompute Inc',
    author_email='support@crosscompute.com',
    url='https://crosscompute.com/docs',
    keywords='web pyramid pylons crosscompute',
    zip_safe=True,
    install_requires=[
        'crosscompute>=0.5.6',
        'crosscompute-integer>=0.5.6',
        'crosscompute-text>=0.5.6',
        'crosscompute-image>=0.5.6',
        'crosscompute-table>=0.5.6',
        'crosscompute-geotable>=0.5.6',
    ])
