import numpy as np
try:
    import pandas
except ImportError:
    from . import _pandas as pandas
from crosscompute.types import DataType
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
        # TODO: Consider support for more geometry types besides points
        # TODO: Consider using a standard class from shapely
        value_by_key = {}

        # TODO: Clean up
        if 'weight' in table.columns:
            weight_column = 'weight'
        elif 'Weight' in table.columns:
            weight_column = 'Weight'
        else:
            weight_column = None

        # We should scale the counts and weights
        count_min, count_max = np.inf, 0
        weight_min, weight_max = np.inf, 0
        for (longitude, latitude), local_table in table.groupby([
                'Longitude', 'Latitude']):

            count = len(local_table)
            if count < count_min:
                count_min = count
            if count > count_max:
                count_max = count

            weight = local_table[weight_column].sum() if weight_column else 0
            if weight < weight_min:
                weight_min = weight
            if weight > weight_max:
                weight_max = weight
            if weight_max == 0:
                weight_max = 1

        for (longitude, latitude), local_table in table.groupby([
                'Longitude', 'Latitude']):
            count = len(local_table)
            weight = local_table[weight_column].sum() if weight_column else 1
            columns = [x for x in local_table.columns if x not in [
                'Longitude', 'Latitude', weight_column]]
            value_by_key[(longitude, latitude)] = {
                'count': (count - count_min) / float(count_max),
                'weight': (weight - weight_min) / float(weight_max),
                'table': local_table[columns],
            }
        return value_by_key
