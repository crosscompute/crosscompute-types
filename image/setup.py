from os.path import abspath, dirname, join
from setuptools import find_packages, setup


ENTRY_POINTS = """
[crosscompute.types]
image = crosscompute_image:ImageType
"""
FOLDER = dirname(abspath(__file__))
DESCRIPTION = '\n\n'.join(open(join(FOLDER, x)).read().strip() for x in [
    'README.rst'])
setup(
    name='crosscompute-image',
    version='0.5.2',
    description='Image data type plugin for CrossCompute',
    long_description=DESCRIPTION,
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Pyramid',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
        'License :: OSI Approved :: MIT License',
    ],
    author='Roy Hyunjin Han',
    author_email='rhh@crosscompute.com',
    url='https://crosscompute.com/docs',
    keywords='web pyramid pylons crosscompute',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'crosscompute>=0.5.2',
    ],
    entry_points=ENTRY_POINTS)
