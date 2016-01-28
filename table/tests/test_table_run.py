from crosscompute.tests import run
from os.path import abspath, dirname, join


TOOL_FOLDER = dirname(abspath(__file__))


def test_run_with_good_table_input():
    standard_output = run(TOOL_FOLDER, 'load-table', {
        'a_table_path': join(TOOL_FOLDER, 'good.csv')})[0]
    assert 'row_count = 3' in standard_output


def test_run_with_bad_table_input():
    standard_output = run(TOOL_FOLDER, 'load-table', {
        'a_table_path': join(TOOL_FOLDER, 'cc.ini')})[0]
    assert 'a_table.error' in standard_output


def test_run_with_bad_table_output():
    standard_output = run(TOOL_FOLDER, 'save-bad-table')[0]
    assert 'b_table.error' in standard_output


if __name__ == '__main__':
    from argparse import ArgumentParser
    argument_parser = ArgumentParser()
    argument_parser.add_argument('--a_table_path')
    argument_parser.add_argument('--save_bad_table', action='store_true')
    args = argument_parser.parse_args()
    if args.a_table_path:
        from crosscompute_table._pandas import read_csv
        table = read_csv(args.a_table_path)
        print('column_count = %s' % len(table.columns))
        print('row_count = %s' % len(table.values))
    if args.save_bad_table:
        print('b_table_path = cc.ini')
