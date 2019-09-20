"""
# PyCRS

PyCRS is a pure Python GIS package for reading, writing, and converting between various
common coordinate reference system (CRS) string and data source formats. 

- [Home Page](http://github.com/karimbahgat/PyCRS)
- [API Documentation](http://pythonhosted.org/PyCRS)

"""

__version__ = "1.0.2"


from . import load
from . import parse
from . import utils
from .elements.cs import CS, GeogCS, ProjCS




