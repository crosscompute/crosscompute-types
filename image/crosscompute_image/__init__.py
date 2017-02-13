from crosscompute.scripts.serve import get_result_file_url
from crosscompute.types import DataType


class ImageType(DataType):
    suffixes = 'image',
    formats = 'jpg', 'png', 'gif'
    template = 'crosscompute_image:type.jinja2'

    @classmethod
    def load(Class, path):
        return path

    @classmethod
    def render(Class, path):
        return get_result_file_url(path)
