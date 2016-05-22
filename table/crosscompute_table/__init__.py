from invisibleroads_macros.disk import get_file_extension
from crosscompute.exceptions import DataTypeError
from crosscompute.scripts.serve import import_upload
from crosscompute.types import DataType
from io import StringIO
from os.path import exists

from .fallbacks import pandas


class TableType(DataType):
    suffixes = 'table',
    formats = 'csv', 'msg', 'json', 'xls', 'xlsx'
    style = 'crosscompute_table:assets/part.min.css'
    script = 'crosscompute_table:assets/part.min.js'
    template = 'crosscompute_table:type.jinja2'
    views = [
        'import_table',
    ]

    @classmethod
    def save(Class, path, table):
        if path.endswith('.csv'):
            table.to_csv(path, index=False)
        elif path.endswith('.msg'):
            table.to_msgpack(path, compress='blosc')
        elif path.endswith('.json'):
            table.to_json(path)
        elif path.endswith('.xls') or path.endswith('.xlsx'):
            table.to_excel(path)
        else:
            raise DataTypeError(
                'file format not supported (%s)' % get_file_extension(path))

    @classmethod
    def load(Class, path):
        if not exists(path):
            raise IOError
        if path.endswith('.csv'):
            table = pandas.read_csv(
                path, encoding='utf-8', skipinitialspace=True)
        elif path.endswith('.msg'):
            table = pandas.read_msgpack(path)
        elif path.endswith('.json'):
            table = pandas.read_json(path, orient='split')
        elif path.endswith('.xls') or path.endswith('.xlsx'):
            table = pandas.read_excel(path)
        else:
            raise DataTypeError(
                'file format not supported (%s)' % get_file_extension(path))
        return table

    @classmethod
    def parse(Class, text):
        try:
            table = pandas.read_csv(
                StringIO(text), encoding='utf-8', skipinitialspace=True)
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


def import_table(request):
    return import_upload(request, TableType, {
        'class': 'editable-table',
    })
