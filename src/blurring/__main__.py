"""The CLI"""
from logging import basicConfig, DEBUG
from argparse import ArgumentParser
from blurring import __version__
from blurring.blur import TheBlur


def main():
    """The command line interface entry point"""
    parser = ArgumentParser(
        description='Censor videos automatically',
        epilog='Copyright 2019 AxJu | blurring v{}'.format(__version__),
    )
    parser.add_argument('src', help='The original video file.')
    parser.add_argument('dest', help='The blurred video file.')
    parser.add_argument('temps', help='The templates to be blurred.')
    parser.add_argument(
        '-t', '--templates', choices=('folder', 'data'), default='data',
        help='Select the template format.',
    )
    parser.add_argument(
        '-d', '--debug',
        help='Set a debug folder.',
    )
    parser.add_argument(
        '-v', '--verbose', action='store_true',
        help='Enable debug infos'
    )
    parser.add_argument(
        '-V', '--version', action='store_true',
        help='Print program version and exit'
    )

    args = parser.parse_args()
    if args.version:
        print(__version__)
        return 1

    if args.verbose:
        log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        basicConfig(level=DEBUG, format=log_format)

    blur = TheBlur()
    blur.add_template(**{args.templates: args.temps})
    if args.debug:
        blur.add_debug(args.debug)
    return blur.run(src=args.src, dest=args.dest)


if __name__ == '__main__':
    main()
