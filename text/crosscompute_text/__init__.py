from crosscompute.types import DataType


class TextType(DataType):
    template = 'crosscompute_text:type.jinja2'
    formats = 'txt',
