from crosscompute.types import DataType, DataTypeError


class IntegerType(DataType):
    suffixes = 'integer', 'int', 'count'
    formats = 'txt',
    template = 'crosscompute_integer:type.jinja2'

    @classmethod
    def save(Class, path, integer):
        open(path, 'w').write(str(integer))

    @classmethod
    def load(Class, path):
        return Class.parse(open(path).read())

    @classmethod
    def parse(Class, text):
        try:
            integer = int(text)
        except (TypeError, ValueError):
            raise DataTypeError('expected integer')
        return integer

    @classmethod
    def format(Class, integer):
        return '%d' % integer
