import numpy as np
from crosscompute.types import DataType
try:
    import pandas
except ImportError:
    from . import _pandas as pandas
from shapely import wkt
from shapely.geometry import mapping
from shapely.geos import ReadingError


GEOMETRY_TYPE_ID_BY_TYPE = {
    'Point': 1,
    'LineString': 2,
    'Polygon': 3,
    'MultiPoint': 4,
    'MultiLineString': 5,
    'MultiPolygon': 6,
}


class GeotableType(DataType):
    formats = 'msg', 'json', 'csv'  # TODO: Add shp.zip
    template = 'crosscompute_geotable:type.jinja2'

    @classmethod
    def load(Class, path):
        if path.endswith('.msg'):
            table = pandas.read_msgpack(path)
        elif path.endswith('.json'):
            table = pandas.read_json(path)
        elif path.endswith('.csv'):
            table = pandas.read_csv(path)
        else:
            raise TypeError('File format not supported (%s)' % path)
        """
        value_by_key = {}

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
        """
        items, properties = [], {}
        geometry_columns = get_geometry_columns(table.columns)
        # If we have latitude and longitude,
        if len(geometry_columns) > 1:
            # Assume all geometries are points
            get_geometry_properties = lambda x: (1, list(x))
        else:
            get_geometry_properties = get_geometry_properties_from_wkt
        for geometry_value, local_table in table.groupby(geometry_columns):
            geometry_type_id, geometry_coordinates = get_geometry_properties(
                geometry_value)
            local_properties = {}
            items.append((
                geometry_type_id, geometry_coordinates, local_properties,
                local_table))
        return items, properties


def get_geometry_columns(columns):
    wkt_columns = filter(lambda x: x.lower().endswith('wkt'), columns)
    if wkt_columns:
        # Assume that WKT coordinate order is (latitude, longitude)
        return np.array(wkt_columns[0]).tolist()
    latitude_columns = filter(is_latitude, columns)
    longitude_columns = filter(is_longitude, columns)
    if latitude_columns and longitude_columns:
        # Use ISO 6709 coordinate order
        return [latitude_columns[0], longitude_columns[0]]


def get_geometry_properties_from_wkt(geometry_wkt):
    try:
        geometry = wkt.loads(geometry_wkt)
    except ReadingError:
        raise TypeError('WKT not parseable (%s)' % geometry_wkt)
    try:
        geometry_type_id = GEOMETRY_TYPE_ID_BY_TYPE[geometry.type]
    except KeyError:
        raise TypeError('Geometry type not supported (%s)' % geometry.type)
    geometry_coordinates = mapping(geometry)['coordinates']
    return geometry_type_id, geometry_coordinates


def is_latitude(column):
    column = column.lower()
    return column.endswith('latitude') or column == 'lat'


def is_longitude(column):
    column = column.lower()
    return column.endswith('longitude') or column == 'lon'
