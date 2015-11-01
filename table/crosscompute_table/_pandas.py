class DummyTable(object):

    def __init__(self, table_csv):
        self.table_csv = table_csv

    def to_csv(self, path=None, index=False):
        if not path:
            return self.table_csv
        open(path, 'wt').write(self.table_csv)


def read_csv(x):
    if hasattr(x, 'read'):
        table_csv = x.read()
    else:
        table_csv = open(x, 'rt').read()
    return DummyTable(table_csv)
