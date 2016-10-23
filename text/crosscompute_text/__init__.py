from crosscompute.types import StringType


class TextType(StringType):
    suffixes = 'text',
    formats = 'txt',
    template = 'crosscompute_text:type.jinja2'
