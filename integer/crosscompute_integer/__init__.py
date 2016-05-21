import msgpack
import simplejson as json
from crosscompute.exceptions import DataTypeError
from crosscompute.types import DataType


class IntegerType(DataType):
    suffixes = 'integer', 'int', 'count', 'length'
    formats = 'msg', 'json', 'txt'
    template = 'crosscompute_integer:type.jinja2'

    @classmethod
    def save(Class, path, integer):
        if path.endswith('.msg'):
            msgpack.pack(integer, open(path, 'w'))
        elif path.endswith('.json'):
            json.dump(integer, open(path, 'w'))
        else:
            open(path, 'w').write(str(integer))

    @classmethod
    def load(Class, path):
        if path.endswith('.msg'):
            integer = msgpack.unpack(open(path))
        elif path.endswith('.json'):
            integer = json.load(open(path))
        else:
            integer = Class.parse(open(path).read())
        return integer

    @classmethod
    def parse(Class, text):
        try:
            integer = int(text)
        except (TypeError, ValueError):
            raise DataTypeError('integer expected (%s)' % text)
        return integer

    @classmethod
    def format(Class, integer):
        return '%d' % integer

    @classmethod
    def match(Class, integer):
        try:
            int(integer)
        except (TypeError, ValueError):
            return False
        return True
