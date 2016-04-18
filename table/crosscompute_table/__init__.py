import pandas
from crosscompute.exceptions import DataTypeError
from crosscompute.types import DataType
from io import StringIO
from os.path import basename


class TableType(DataType):
    suffixes = 'table',
    formats = 'msg', 'json', 'csv', 'xls', 'xlsx'
    asset_paths = [
        'mindmup-editabletable.min.js',
    ]
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
            raise DataTypeError(
                'File format not supported (%s)' % basename(path))

    @classmethod
    def load(Class, path):
        if path.endswith('.msg'):
            table = pandas.read_msgpack(path)
        elif path.endswith('.json'):
            table = pandas.read_json(path, orient='split')
        elif path.endswith('.csv'):
            table = pandas.read_csv(path, skipinitialspace=True)
        elif path.endswith('.xls') or path.endswith('.xlsx'):
            table = pandas.read_excel(path)
        else:
            raise DataTypeError(
                'File format not supported (%s)' % basename(path))
        return table

    @classmethod
    def parse(Class, text):
        try:
            table = pandas.read_csv(StringIO(text), skipinitialspace=True)
        except (TypeError, ValueError):
            raise TypeError('expected_table')
        return table

    @classmethod
    def format(Class, table, format_name='csv'):
        if format_name == 'csv':
            return table.to_csv(index=False)
        elif format_name == 'json':
            return table.to_json(orient='split')

    @classmethod
    def match(Class, table):
        return hasattr(table, 'iterrows')
