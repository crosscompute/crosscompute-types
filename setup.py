from os.path import abspath, dirname, join
from setuptools import setup


FOLDER = dirname(abspath(__file__))
DESCRIPTION = '\n\n'.join(open(join(FOLDER, x)).read().strip() for x in [
    'README.rst'])
setup(
    name='crosscompute-types',
    version='0.6.2',
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
        'crosscompute>=0.6.2',
        'crosscompute-integer>=0.6.0',
        'crosscompute-text>=0.6.0',
        'crosscompute-image>=0.6.0',
        'crosscompute-table>=0.6.1',
        'crosscompute-geotable>=0.6.1',
    ])
