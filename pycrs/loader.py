
import json
import urllib2
from . import parser


#################
# USER FUNCTIONS
#################

# convenience methods for loading from different sources

def from_url(url, format=None):
    # first get string from url
    string = urllib2.urlopen(url).read()

    # then determine parser
    if format:
        # user specified format
        format = format.lower().replace(" ", "_")
        func = parser.__getattr__("from_%s" % format)
    else:
        # unknown format
        func = parser.from_unknown_text

    # then load
    crs = func(string)
    return crs

def from_file(filepath):
    if filepath.endswith(".prj"):
        string = open(filepath, "r").read()
        return parser.from_esri_wkt(string)
    
    elif filepath.endswith((".geojson",".json")):
        crsinfo = json.load(filepath)["crs"]
        
        if crsinfo["type"] == "name":
            string = crsinfo["properties"]["name"]
            return parser.from_unknown_text(string)
            
        elif crsinfo["type"] == "link":
            url = crsinfo["properties"]["name"]
            type = crsinfo["properties"].get("type")
            return from_url(url, format=type)
            
        else: raise Exception("invalid geojson crs type: must be either name or link")

##    elif filepath.endswith((".tif",".tiff",".geotiff")):
##        pass
##        # ...




                                      
        
