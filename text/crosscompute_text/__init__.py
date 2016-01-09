from crosscompute.types import DataType


class TextType(DataType):
    formats = 'txt',
    template = 'crosscompute_text:type.jinja2'
