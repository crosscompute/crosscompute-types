import msgpack
import simplejson as json
from crosscompute.types import DataType
from os.path import splitext


class IntegerType(DataType):
    template = 'crosscompute_integer:type.jinja2'
    file_formats = ['msg', 'json', 'txt']

    def save(self, path, integer):
        extension = splitext(path)[1]
        if '.msg' == extension:
            msgpack.pack(integer, open(path, 'wb'))
        elif '.json' == extension:
            json.dump(integer, open(path, 'wt'))
        else:
            open(path, 'wt').write(str(integer))

    def load(self, path):
        extension = splitext(path)[1]
        if '.msg' == extension:
            integer = msgpack.unpack(open(path, 'rb'))
        elif '.json' == extension:
            integer = json.load(open(path, 'rt'))
        else:
            integer = self.parse(open(path, 'rt').read())
        return integer

    def parse(self, text):
        try:
            integer = int(text)
        except (TypeError, ValueError):
            raise TypeError('expected_integer')
        return integer

    def format(self, integer):
        return '%d' % self.parse(integer)
