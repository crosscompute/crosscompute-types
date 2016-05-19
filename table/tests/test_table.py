from crosscompute.tests import run


def test_good_input(tmpdir):
    args = str(tmpdir), 'load-table', {'a_table_path': 'good.csv'}
    r = run(*args)
    assert r['standard_outputs']['row_count'] == 3


if __name__ == '__main__':
    from argparse import ArgumentParser
    argument_parser = ArgumentParser()
    argument_parser.add_argument('--a_table_path')
    args = argument_parser.parse_args()
    if args.a_table_path:
        from pandas import read_csv
        table = read_csv(args.a_table_path)
        print('column_count = %s' % len(table.columns))
        print('row_count = %s' % len(table.values))
