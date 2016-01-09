try:
    import pandas
except ImportError:
    from . import _pandas as pandas
from crosscompute.types import DataType
from io import StringIO


class TableType(DataType):
    formats = 'msg', 'json', 'csv', 'xls', 'xlsx'
    template = 'crosscompute_table:type.jinja2'

    @classmethod
    def save(Class, path, table):
        if path.endswith('.msg'):
            table.to_msgpack(path, compress='blosc')
        elif path.endswith('.json'):
            table.to_json(path)
        elif path.endswith('.csv'):
            table.to_csv(path, index=False)
        elif path.endswith('.xls') or path.endswith('.xlsx'):
            table.to_excel(path)
        else:
            raise TypeError('unsupported_format')

    @classmethod
    def load(Class, path):
        if path.endswith('.msg'):
            table = pandas.read_msgpack(path)
        elif path.endswith('.json'):
            table = pandas.read_json(path)
        elif path.endswith('.csv'):
            table = pandas.read_csv(path, skipinitialspace=True)
        elif path.endswith('.xls') or path.endswith('.xlsx'):
            table = pandas.read_excel(path)
        else:
            raise TypeError('unsupported_format')
        return table

    @classmethod
    def parse(Class, text):
        try:
            table = pandas.read_csv(StringIO(text), skipinitialspace=True)
        except (TypeError, ValueError):
            raise TypeError('expected_table')
        return table

    @classmethod
    def format(Class, table):
        return table.to_csv(index=False)

    @classmethod
    def match(Class, table):
        return hasattr(table, 'iterrows')
