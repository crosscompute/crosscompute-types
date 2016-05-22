import codecs
from collections import defaultdict
import csv
from six import StringIO


class Array(object):

    def __init__(self, values):
        self.values = values
        self.size = len(values)

    def __getitem__(self, index):
        if not hasattr(index, '__iter__'):
            return self.values[index]
        return Array([self.values[i] for i in index])

    def __len__(self):
        return len(self.values)

    def __div__(self, scalar):
        return Array([x / float(scalar) for x in self.values])

    def __truediv__(self, scalar):
        return self.__div__(scalar)

    def sum(self, axis=None):
        if not self.values:
            return 0
        if not isinstance(self.values[0], Array) or axis is None:
            return sum(float(x) for x in self.values)
        values = []
        for index in range(len(self.values[0])):
            total = 0
            for row_values in self.values:
                total += row_values[index]
            values.append(total)
        return Array(values)

    def mean(self):
        return self.sum() / float(self.size)


class Series(Array):

    def apply(self, func):
        return Series([func(x) for x in self.values])

    def sum(self):
        return super(Series, self).sum(axis=1)


class DataFrame(object):

    def __init__(self, values, columns):
        self.values = values
        self.columns = columns

    def __getitem__(self, key):
        if isinstance(key, slice):
            return DataFrame(
                self.values[key.start:key.stop:key.step], self.columns)
        return self.values[key]

    def __len__(self):
        return len(self.values)

    def fillna(self, value):
        return self

    def iterrows(self):
        return enumerate(self.values)

    def to_csv(self, path=None, index=False):
        if path:
            csv_writer = csv.writer(open(path, 'w'))
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

    def groupby(self, by):
        values_by_key = defaultdict(list)
        for row_values in self.values:
            key = []
            for column_name in by:
                column_index = self.columns.index(column_name)
                column_value = row_values[column_index]
                key.append(column_value)
            key = tuple(key) if len(key) > 1 else key[0]
            values_by_key[key].append(row_values)
        for key, values in values_by_key.items():
            yield key, DataFrame(values, list(self.columns))

    def drop(self, labels, axis=0):
        if axis != 1:
            raise NotImplementedError
        for column_name in labels:
            self.pop(column_name)
        return self

    def pop(self, item):
        column_values = []
        column_index = self.columns.index(item)
        for row_values in self.values:
            column_values.append(row_values.pop(column_index))
        self.columns.pop(column_index)
        return Series(column_values)


def read_csv(x, encoding='utf-8', skipinitialspace=False):
    table_csv = x.read() if hasattr(x, 'read') else codecs.open(
        x, encoding=encoding).read()
    csv_reader = csv.reader(table_csv.strip().splitlines())
    try:
        columns = next(csv_reader)
    except StopIteration:
        columns = []
    if skipinitialspace:
        columns = [c.lstrip() for c in columns]
    values = []
    for row_values in list(csv_reader):
        values.append([_parse_value(_) for _ in row_values])
    return DataFrame(values, columns)


def _parse_value(x):
    try:
        return int(x)
    except ValueError:
        pass
    try:
        return float(x)
    except ValueError:
        pass
    return x
