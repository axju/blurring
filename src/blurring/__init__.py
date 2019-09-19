"""nothing to say here"""
from pkg_resources import get_distribution, DistributionNotFound


__version__ = 'unknown'
try:
    __version__ = get_distribution(__name__).version
finally:
    del get_distribution, DistributionNotFound
