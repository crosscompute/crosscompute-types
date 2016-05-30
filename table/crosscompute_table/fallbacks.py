try:
    import pandas
except ImportError:
    from . import _pandas as pandas
    print('Please install pandas for full table support')
