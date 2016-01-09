import numpy as np
try:
    import pandas
except ImportError:
    from . import _pandas as pandas
from crosscompute.types import DataType
from os import environ


MAPBOX_TOKEN = environ.get(
    'MAPBOX_TOKEN', 'pk.eyJ1IjoibWFwYm94IiwiYSI6IjZjNmRjNzk3ZmE2MTcwOTEwMGY0MzU3YjUzOWFmNWZhIn0.Y8bhBaUMqFiPrDRW9hieoQ')  # noqa


class GeotableType(DataType):
    formats = 'msg', 'json', 'csv'  # TODO: Add shp.zip
    template = 'crosscompute_geotable:type.jinja2'

    @classmethod
    def get_template_variables(Class):
        return {'mapbox_token': MAPBOX_TOKEN}

    @classmethod
    def load(Class, path):
        if path.endswith('.msg'):
            table = pandas.read_msgpack(path)
        elif path.endswith('.json'):
            table = pandas.read_json(path)
        elif path.endswith('.csv'):
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
