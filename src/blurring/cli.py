"""Some command line functions"""
import os
from logging import basicConfig, DEBUG
from argparse import ArgumentParser
from blurring import __version__
from blurring.blur import Blurring
from blurring.utils import TempGen


def create_blurred_video(argv=None):
    """The command line Blurring entry point"""
    parser = ArgumentParser(
        description='Censor videos automatically',
        epilog='Copyright 2019 AxJu | blurring v{}'.format(__version__),
    )
    parser.add_argument('src', help='The original video file.')
    parser.add_argument('dest', help='The blurred video file.')
    parser.add_argument('temps', help='The templates to be blurred.')
    parser.add_argument(
        '-t', '--templates', choices=('file', 'folder', 'data'), default='file',
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

    args = parser.parse_args(argv)
    if args.version:
        print(__version__)
        return 1

    if args.verbose:
        log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        basicConfig(level=DEBUG, format=log_format)

    blur = Blurring()
    blur.add_template(**{args.templates: args.temps})
    if args.debug:
        blur.add_debug(args.debug)
    return blur.run(src=args.src, dest=args.dest)


def create_template(argv=None):
    """cli for creating a template"""
    parser = ArgumentParser(
        description='Create a tempalte image',
        epilog='Copyright 2019 AxJu | blurring v{}'.format(__version__),
    )
    parser.add_argument('filename', help='The templates filename, without the extension!')

    args = parser.parse_args(argv)

    filename = os.path.abspath(args.filename)
    folder = os.path.dirname(filename)
    name = os.path.splitext(filename)[0]

    data = {
        'text': 'PASSWORD',
        'height': 18, 'width': 70,
        'scale': 0.4, 'font': 0,
        'pos_x': 0, 'pos_y': 12,
    }
    for key, default in data.items():
        data[key] = input('{} [{}]: '.format(key, default)) or default

    data['kind'] = 'cv2'
    data['name'] = name
    data['scale'] = float(data['scale'])
    data['font'] = int(data['font'])
    data['pos'] = (int(data['pos_x']), int(data['pos_y']))
    data['size'] = (int(data['height']), int(data['width']))

    tempgen = TempGen(folder=folder, data=data)
    tempgen.run()
