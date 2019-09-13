"""The CLI"""
from logging import basicConfig, DEBUG
from argparse import ArgumentParser
from blurring import __version__


def main():
    """The command line interface entry point"""
    parser = ArgumentParser(
        description='Censor videos automatically',
        epilog='Copyright 2019 AxJu | blurring v{}'.format(__version__),
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

    return 1


if __name__ == '__main__':
    main()
