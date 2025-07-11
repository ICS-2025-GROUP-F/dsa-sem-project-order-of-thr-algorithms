# Export main classes for public API
from .gui.MainWindow import MainApplication
from .database.DBOperations import DBOperations

# Optional: Package metadata
__version__ = "1.0.0"
__author__ = "Mark Mbithi <mark.mbiti@strathmore.edu>"

# Explicitly declare public symbols
__all__ = [
    'MainApplication',
    'DBOperations'
]