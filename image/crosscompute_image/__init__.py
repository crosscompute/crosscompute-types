from crosscompute.types import DataType


class ImageType(DataType):
    template = 'crosscompute_image:type.jinja2'
    file_formats = ['jpg', 'png', 'gif']

    def load(self, path):
        return path
