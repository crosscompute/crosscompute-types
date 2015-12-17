try:
    import pandas
except ImportError:
    from . import _pandas as pandas
from crosscompute.types import DataType
from io import StringIO
from os.path import splitext


class GeotableType(DataType):
    template = 'crosscompute_geotable:type.jinja2'
    file_formats = ['msg', 'json', 'csv']  # TODO: Add shp.zip

    def load(self, path):
        extension = splitext(path)[1]
        if '.msg' == extension:
            table = pandas.read_msgpack(path)
        elif '.json' == extension:
            table = pandas.read_json(path)
        elif '.csv' == extension:
            table = pandas.read_csv(path)
        else:
            raise TypeError('unsupported_format')
        return table
