"""The CLI"""
import sys
from blurring.cli import create_blurred_video


if __name__ == '__main__':
    create_blurred_video(sys.argv[1:])
