from crosscompute.types import DataType


class ImageType(DataType):
    template = 'crosscompute_image:type.jinja2'
    formats = 'jpg', 'png', 'gif'

    @classmethod
    def load(Class, path):
        return path
