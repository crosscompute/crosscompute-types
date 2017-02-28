import chardet
import pandas as pd
from invisibleroads_macros.disk import get_file_extension
from crosscompute.exceptions import DataTypeError
from crosscompute.scripts.serve import import_upload
from crosscompute.types import DataType
from io import StringIO
from os.path import exists


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
            table.to_csv(path, encoding='utf-8', index=False)
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
            try:
                table = pd.read_csv(
                    path, encoding='utf-8', skipinitialspace=True)
            except UnicodeDecodeError:
                encoding = _get_encoding(open(path).read())
                table = pd.read_csv(
                    path, encoding=encoding, skipinitialspace=True)
        elif path.endswith('.msg'):
            table = pd.read_msgpack(path)
        elif path.endswith('.json'):
            table = pd.read_json(path, orient='split')
        elif path.endswith('.xls') or path.endswith('.xlsx'):
            table = pd.read_excel(path)
        else:
            raise DataTypeError(
                'file format not supported (%s)' % get_file_extension(path))
        return table

    @classmethod
    def parse(Class, text):
        return pd.read_csv(
            StringIO(text), encoding='utf-8', skipinitialspace=True)

    @classmethod
    def render(Class, table, format_name='csv'):
        if format_name == 'csv':
            return table.to_csv(encoding='utf-8', index=False)
        elif format_name == 'json':
            return table.to_json(orient='split')


def import_table(request):
    return import_upload(request, TableType, {'class': 'editable'})


def _get_encoding(content):
    best_encoding = chardet.detect(content)['encoding']
    best_alpha_count = 0
    for encoding in [best_encoding, 'cp850']:
        alpha_count = sum(x.isalpha() for x in content.decode(encoding))
        if alpha_count > best_alpha_count:
            best_encoding = encoding
            best_alpha_count = alpha_count
    return best_encoding
