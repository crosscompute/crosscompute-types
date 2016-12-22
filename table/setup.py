from os.path import abspath, dirname, join
from setuptools import find_packages, setup


ENTRY_POINTS = """
[crosscompute.types]
table = crosscompute_table:TableType
"""
FOLDER = dirname(abspath(__file__))
DESCRIPTION = '\n\n'.join(open(join(FOLDER, x)).read().strip() for x in [
    'README.rst'])
setup(
    name='crosscompute-table',
    version='0.6.1',
    description='Table data type plugin for CrossCompute',
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
    setup_requires=[
        'pytest-runner',
    ],
    install_requires=[
        'chardet',
        'crosscompute>=0.6.1',
        'six',
    ],
    tests_require=[
        'pytest',
    ],
    entry_points=ENTRY_POINTS)
