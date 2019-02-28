"""
Convenience functions for loading from different sources.
"""

import json
import sys
try:
    import urllib.request as urllib2
except ImportError:
    import urllib2
from . import parse

PY3 = (int(sys.version_info[0]) > 2)

class FormatError(Exception):
    pass

#################
# USER FUNCTIONS
#################

def from_url(url, format=None):
    """
    Returns the crs object from a string interpreted as a specified format, located at a given url site.

    Arguments:

    - *url*: The url where the crs string is to be read from. 
    - *format* (optional): Which format to parse the crs string as. One of "ogc wkt", "esri wkt", or "proj4".
        If None, tries to autodetect the format for you (default).

    Returns:

    - CRS object.
    """
    # first get string from url
    string = urllib2.urlopen(url).read()
    
    if PY3 is True:
        # decode str into string
        string = string.decode('utf-8')

    # then determine parser
    if format:
        # user specified format
        format = format.lower().replace(" ", "_")
        func = parse.__getattr__("from_%s" % format)
    else:
        # unknown format
        func = parse.from_unknown_text

    # then load
    crs = func(string)
    return crs

def from_file(filepath):
    """
    Returns the crs object from a file, with the format determined from the filename extension.

    Arguments:

    - *filepath*: filepath to be loaded, including extension. 
    """
    if filepath.endswith(".prj"):
        string = open(filepath, "r").read()
        return parse.from_unknown_wkt(string)
    
    elif filepath.endswith((".geojson",".json")):
        raw = open(filepath).read()
        geoj = json.loads(raw)
        if "crs" in geoj:
            crsinfo = geoj["crs"]
            
            if crsinfo["type"] == "name":
                string = crsinfo["properties"]["name"]
                return parse.from_unknown_text(string)
                
            elif crsinfo["type"] == "link":
                url = crsinfo["properties"]["name"]
                type = crsinfo["properties"].get("type")
                return from_url(url, format=type)
                
            else: raise FormatError("Invalid GeoJSON crs type: must be either 'name' or 'link'")

        else:
            # assume default wgs84 as per the spec
            return parse.from_epsg_code("4326")

##    elif filepath.endswith((".tif",".tiff",".geotiff")):
##        pass
##        # ...




                                      
        
