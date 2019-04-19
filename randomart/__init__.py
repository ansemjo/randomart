try:
  from .__metadata__ import VERSION as __version__
except ImportError:
  __version__ = "development"