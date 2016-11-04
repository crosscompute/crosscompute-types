from crosscompute.exceptions import DataTypeError


RGB_BY_NAME = {
    'b': (0.00, 0.00, 1.00),
    'g': (0.00, 0.50, 0.00),
    'r': (1.00, 0.00, 0.00),
    'c': (0.00, 0.75, 0.75),
    'm': (0.75, 0.00, 0.75),
    'y': (0.75, 0.75, 0.00),
    'k': (0.00, 0.00, 0.00),
    'w': (1.00, 1.00, 1.00),
    'brown': (0.6470588235294118, 0.16470588235294117, 0.16470588235294117),
    'violet': (0.9333333333333333, 0.5098039215686274, 0.9333333333333333),
    'purple': (0.5019607843137255, 0.0, 0.5019607843137255),
    'orange': (1.0, 0.6470588235294118, 0.0),
}
RGB_BY_NAME['blue'] = RGB_BY_NAME['b']
RGB_BY_NAME['green'] = RGB_BY_NAME['g']
RGB_BY_NAME['red'] = RGB_BY_NAME['r']
RGB_BY_NAME['cyan'] = RGB_BY_NAME['c']
RGB_BY_NAME['magenta'] = RGB_BY_NAME['m']
RGB_BY_NAME['yellow'] = RGB_BY_NAME['y']
RGB_BY_NAME['black'] = RGB_BY_NAME['k']
RGB_BY_NAME['white'] = RGB_BY_NAME['w']


class ColorConverter(object):

    def to_rgb(self, x):
        try:
            x_float = float(x)
        except ValueError:
            if x.startswith('#'):
                return _hex2rgb(x)
            try:
                return RGB_BY_NAME[x]
            except KeyError:
                raise ValueError('could not parse color (%s)' % x)
        if x_float < 0 or x_float > 1:
            raise ValueError('gray value must be between 0 and 1 (%s)' % x)
        return (x_float,) * 3


def _hex2rgb(x):
    return tuple([int(n, 16) / 255. for n in (x[1:3], x[3:5], x[5:7])])


def _rgb2hex(x):
    return '#%02x%02x%02x' % tuple(int(round(val * 255)) for val in x[:3])


try:
    from matplotlib.colors import colorConverter, rgb2hex
    from numpy import array
except ImportError:
    from crosscompute_table._pandas import Array
    colorConverter = ColorConverter()
    rgb2hex = _rgb2hex
    array = Array
    print('Please install matplotlib for full color support')
try:
    import geometryIO  # noqa
except ImportError:
    print('Please install GDAL, shapely, geometryIO for shapefile support')


try:
    from shapely import wkt
except ImportError:
    import re

    WKT_PATTERN = re.compile(r'([A-Za-z]+)\s*\(([0-9 -.,()]*)\)')
    SEQUENCE_PATTERN = re.compile(r'\(([0-9 -.,()]*?)\)')

    def _parse_geometry(geometry_wkt):
        try:
            geometry_type, xys_string = WKT_PATTERN.match(
                geometry_wkt).groups()
        except AttributeError:
            raise DataTypeError('wkt not parseable (%s)' % geometry_wkt)
        geometry_type = geometry_type.upper()
        try:
            geometry_type_id = {
                'POINT': 1,
                'LINESTRING': 2,
                'MULTILINESTRING': 3,
            }[geometry_type]
        except KeyError:
            raise DataTypeError(
                'geometry type not supported (%s)' % geometry_type)
        if geometry_type_id == 1:
            geometry_coordinates = _parse_geometry_coordinates(xys_string)[0]
        elif geometry_type_id == 2:
            geometry_coordinates = _parse_geometry_coordinates(xys_string)
        else:
            xys_strings = SEQUENCE_PATTERN.findall(xys_string)
            geometry_coordinates = [
                _parse_geometry_coordinates(_) for _ in xys_strings]
        return geometry_type_id, geometry_coordinates

    def _parse_geometry_coordinates(xys_string):
        geometry_coordinates = []
        for xy_string in xys_string.split(','):
            x, y = xy_string.strip().split(' ')[:2]
            try:
                x, y = int(x), int(y)
            except ValueError:
                x, y = float(x), float(y)
            geometry_coordinates.append([x, y])
        return geometry_coordinates

    print('Please install shapely for extended geometry support')
else:
    def _parse_geometry(geometry_wkt):
        geometry = wkt.loads(geometry_wkt)
        geometry_type = geometry.type.upper()
        if geometry_type == 'POINT':
            geometry_type_id = 1
            geometry_coordinates = list(geometry.coords[0][:2])
        elif geometry_type == 'LINESTRING':
            geometry_type_id = 2
            geometry_coordinates = [list(x[:2]) for x in geometry.coords]
        elif geometry_type == 'MULTILINESTRING':
            geometry_type_id = 3
            geometry_coordinates = [[
                list(x[:2]) for x in geom.coords] for geom in geometry.geoms]
        else:
            raise DataTypeError(
                'geometry type not supported (%s)' % geometry_type)
        return geometry_type_id, geometry_coordinates
