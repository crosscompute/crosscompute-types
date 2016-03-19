from os.path import abspath, dirname, join
from setuptools import find_packages, setup


FOLDER = dirname(abspath(__file__))
DESCRIPTION = '\n\n'.join(open(join(FOLDER, x)).read().strip() for x in [
    'CHANGES.rst',
    'README.rst'])
setup(
    name='crosscompute-geotable',
    version='0.0.2',
    description='Geotable data type plugin for CrossCompute',
    long_description=DESCRIPTION,
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Pyramid',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
        'License :: OSI Approved :: MIT License',
    ],
    author='Roy Hyunjin Han',
    author_email='rhh@crosscompute.com',
    url='https://crosscompute.com',
    keywords='web pyramid pylons invisibleroads crosscompute',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'crosscompute>=0.4.0',
        'matplotlib',
        'numpy',
        'shapely',
    ],
    entry_points={
        'crosscompute.types': [
            'geotable = crosscompute_geotable:GeotableType',
        ],
    })
