from crosscompute.types import DataType


class ImageType(DataType):
    formats = 'jpg', 'png', 'gif'
    template = 'crosscompute_image:type.jinja2'

    @classmethod
    def load(Class, path):
        return path
