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
            return RGB_BY_NAME[x]
        except KeyError:
            raise ValueError('could not parse color (%s)' % x)


try:
    from matplotlib.colors import colorConverter
    from numpy import array
except ImportError:
    from crosscompute_table._pandas import Array
    colorConverter = ColorConverter()
    array = Array
    print('Please install matplotlib for full color support')
try:
    import geometryIO
except ImportError:
    print('Please install GDAL, shapely, geometryIO for shapefile support')
