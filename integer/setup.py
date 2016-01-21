from os.path import abspath, dirname, join
from setuptools import find_packages, setup


FOLDER = dirname(abspath(__file__))
DESCRIPTION = '\n\n'.join(open(join(FOLDER, x)).read().strip() for x in [
    'README.rst'])
setup(
    name='crosscompute-integer',
    version='0.3.1',
    description='Integer data type plugin for CrossCompute',
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
    setup_requires=[
        'pytest-runner',
    ],
    install_requires=[
        'crosscompute>=0.4.0',
        'msgpack-python',
        'simplejson',
    ],
    tests_require=[
        'pytest',
    ],
    entry_points={
        'crosscompute.types': [
            'count = crosscompute_integer:IntegerType',
            'integer = crosscompute_integer:IntegerType',
            'length = crosscompute_integer:IntegerType',
        ],
    })
