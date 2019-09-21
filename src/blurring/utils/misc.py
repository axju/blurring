"""Some nice tools"""
import os
import ffmpeg


def create_frames(src, dest, basename='%06d.png'):
    """Extract all frames from a video file."""
    stream = ffmpeg.input(src)
    stream = ffmpeg.output(stream, os.path.join(dest, basename))
    ffmpeg.run(stream, overwrite_output=True, quiet=True)


def save_frames(src, dest, basename='%06d.png'):
    """Create a video file from individual frames"""
    stream = ffmpeg.input(os.path.join(src, basename))
    stream = ffmpeg.output(stream, dest)
    ffmpeg.run(stream, overwrite_output=True, quiet=True)


def find_area(data, area):
    """Return the index of the area in the data list"""
    for index, values in enumerate(data):
        if values.get('area') == area:
            return index
    return -1
