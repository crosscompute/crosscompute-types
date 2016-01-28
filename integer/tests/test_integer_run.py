from crosscompute.tests import run
from os.path import abspath, dirname


TOOL_FOLDER = dirname(abspath(__file__))


def test_run_with_good_integer_input():
    standard_output = run(TOOL_FOLDER, 'load-integer', {'x_integer': 2})[0]
    assert 'xx_integer = 4' in standard_output


def test_run_with_bad_integer_input():
    standard_output = run(TOOL_FOLDER, 'load-integer', {'x_integer': 'abc'})[0]
    assert 'x_integer.error' in standard_output


def test_run_with_bad_integer_output():
    standard_output = run(TOOL_FOLDER, 'save-bad-integer')[0]
    assert 'z_integer.error' in standard_output


if __name__ == '__main__':
    from argparse import ArgumentParser
    argument_parser = ArgumentParser()
    argument_parser.add_argument('--x_integer')
    argument_parser.add_argument('--y_integer')
    argument_parser.add_argument('--save_bad_integer', action='store_true')
    args = argument_parser.parse_args()
    if args.x_integer:
        xx_integer = int(args.x_integer) ** 2
        print('xx_integer = %s' % xx_integer)
    if args.y_integer:
        yy_integer = int(args.y_integer) ** 2
        print('yy_integer = %s' % yy_integer)
    if args.save_bad_integer:
        print('z_integer = abc')
