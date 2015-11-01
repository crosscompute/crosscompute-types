import csv
from cStringIO import StringIO


class DummyTable(object):

    def __init__(self, table_csv):
        csv_reader = csv.reader(table_csv.strip().splitlines())
        try:
            self.columns = csv_reader.next()
        except StopIteration:
            self.columns = []
        self.values = []
        for row in csv_reader:
            self.values.append(row)

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
            s.reset()
            return s.read()


def read_csv(x):
    if hasattr(x, 'read'):
        table_csv = x.read()
    else:
        table_csv = open(x, 'rt').read()
    return DummyTable(table_csv)
