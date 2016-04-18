from crosscompute.types import DataType


class TextType(DataType):
    suffixes = 'text',
    formats = 'txt',
    template = 'crosscompute_text:type.jinja2'
