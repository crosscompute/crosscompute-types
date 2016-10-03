from os.path import abspath, dirname, join
from setuptools import find_packages, setup


ENTRY_POINTS = """
[crosscompute.types]
geotable = crosscompute_geotable:GeotableType
"""
FOLDER = dirname(abspath(__file__))
DESCRIPTION = '\n\n'.join(open(join(FOLDER, x)).read().strip() for x in [
    'CHANGES.rst', 'README.rst'])
setup(
    name='crosscompute-geotable',
    version='0.5.3.5',
    description='Geotable data type plugin for CrossCompute',
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
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'crosscompute>=0.5.4',
        'crosscompute_table>=0.5.3.3',
        'invisibleroads_macros>=0.7.1',
    ],
    entry_points=ENTRY_POINTS)
