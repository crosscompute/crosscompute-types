from crosscompute.tests import run, serve_bad_request


def test_good_input(tmpdir):
    args = str(tmpdir), 'load-integer', {'x_integer': 2}
    r = run(*args)
    r['standard_outputs']['xx_integer'] == 4


def test_bad_input(tmpdir):
    args = str(tmpdir), 'load-integer', {'x_integer': 'abc'}
    errors = serve_bad_request(*args)
    assert 'x_integer' in errors


def test_bad_output(tmpdir):
    args = str(tmpdir), 'save-bad-integer'
    r = run(*args)
    assert 'z_integer.error' in r['type_errors']


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
