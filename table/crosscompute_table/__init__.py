try:
    import pandas
except ImportError:
    from . import _pandas as pandas
from crosscompute.types import DataType
from io import StringIO
from os.path import splitext


class TableType(DataType):
    template = 'crosscompute_table:type.jinja2'
    file_formats = ['msg', 'json', 'csv', 'xls', 'xlsx']

    def save(self, path, table):
        extension = splitext(path)[1]
        if '.msg' == extension:
            table.to_msgpack(path, compress='blosc')
        elif '.json' == extension:
            table.to_json(path)
        elif '.csv' == extension:
            table.to_csv(path, index=False)
        elif extension in ('.xls', '.xlsx'):
            table.to_excel(path)
        else:
            raise TypeError('unsupported_format')

    def load(self, path):
        extension = splitext(path)[1]
        if '.msg' == extension:
            table = pandas.read_msgpack(path)
        elif '.json' == extension:
            table = pandas.read_json(path)
        elif '.csv' == extension:
            table = pandas.read_csv(path)
        elif extension in ('.xls', '.xlsx'):
            table = pandas.read_excel(path)
        else:
            raise TypeError('unsupported_format')
        return table

    def parse(self, text):
        try:
            table = pandas.read_csv(StringIO(text))
        except (TypeError, ValueError):
            raise TypeError('expected_table')
        return table

    def format(self, table):
        return table.to_csv(index=False)
