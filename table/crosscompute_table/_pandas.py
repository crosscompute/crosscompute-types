import csv
from io import StringIO


class DummyTable(object):

    def __init__(self, values, columns):
        self.values = values
        self.columns = columns

    def __getitem__(self, key):
        if isinstance(key, slice):
            return DummyTable(
                self.values[key.start:key.stop:key.step], self.columns)
        return self.values[key]

    def iterrows(self):
        return enumerate(self.values)

    def to_csv(self, path=None, index=False):
        if path:
            csv_writer = csv.writer(open(path, 'wt'))
        else:
            s = StringIO()
            csv_writer = csv.writer(s)
        if self.columns:
            csv_writer.writerow(self.columns)
        for row in self.values:
            csv_writer.writerow(row)
        if not path:
            s.seek(0)
            return s.read()


def read_csv(x):
    table_csv = x.read() if hasattr(x, 'read') else open(x, 'rt').read()
    csv_reader = csv.reader(table_csv.strip().splitlines())
    try:
        columns = next(csv_reader)
    except StopIteration:
        columns = []
    return DummyTable(list(csv_reader), columns)
