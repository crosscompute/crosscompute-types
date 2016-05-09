from crosscompute.scripts.serve import get_file_url
from crosscompute.types import DataType


class ImageType(DataType):
    suffixes = 'image',
    formats = 'jpg', 'png', 'gif'
    template = 'crosscompute_image:type.jinja2'

    @classmethod
    def load(Class, path):
        return path

    @classmethod
    def format(Class, path):
        return get_file_url(path)
