
import json


#################
# USER FUNCTIONS
#################


# parse from text strings
# possible use module: https://github.com/rockdoc/grabbag/wiki/CRS-WKT-Parser
# also note some paramter descriptions: http://www.geoapi.org/3.0/javadoc/org/opengis/referencing/doc-files/WKT.html
# and see gdal source code: http://gis.stackexchange.com/questions/129764/how-are-esri-wkt-projections-different-from-ogc-wkt-projections

def from_epsg_code(string):
    # must go online (or look up local table) to get crs details
    pass

def from_esri_code(string):
    # must go online (or look up local table) to get crs details
    pass

def from_sr_code(string):
    # must go online (or look up local table) to get crs details
    pass

def from_esri_wkt(string):
    # parse arguments into components
    # use args to create crs
    pass
        
def from_ogc_wkt(string):
    # parse arguments into components
    # use args to create crs
    pass

def from_unknown_wkt(string):
    # detect if ogc wkt or esri wkt
    # TIPS: esri wkt datums all use "D_" before the datum name
    # then load with appropriate function
    pass

def from_proj4(string):
    # parse arguments into components
    # use args to create crs
    pass

def from_ogc_urn(string):
    # hmmm, seems like ogc urn could be anything incl online link, epsg, etc...
    # if necessary, must go online (or lookup local table) to get details
    # maybe test which of these and run their function? 
    pass

def from_unknown_text(text):
    # detect type and load with appropriate function
    
    if string.startswith("urn:"):
        from_ogc_urn(string)

    elif string.startswith("+proj="):
        from_proj4(string)

    elif string.startswith("PROJCS["):
        from_unknown_wkt(string)

    elif string.startswith("EPSG:"):
        from_epsg_code(string)

    elif string.startswith("ESRI:"):
        from_esri_code(string)

    elif string.startswith("SR-ORG:"):
        from_sr_code(string)

    else: raise Exception("Could not detect which type of crs")

def from_geotiff_params(**params):
    pass




# convenience methods for loading from different sources

def from_url(url, format=None):
    # first get string from url
    # ...

    # then load
    if format:
        # load string using specified format
        pass
    else:
        from_unknown_text(string)

def from_file(filepath):
    if filepath.endswith(".prj"):
        string = open(filepath, "r").read()
        from_esri_wkt(string)
    
    elif filepath.endswith((".geojson",".json")):
        crsinfo = json.load(filepath)["crs"]
        
        if crsinfo["type"] == "name":
            string = crsinfo["properties"]["name"]
            from_unknown_text(string)
            
        elif crsinfo["type"] == "link":
            url = crsinfo["properties"]["name"]
            type = crsinfo["properties"].get("type")
            from_url(url, format=type)
            
        else: raise Exception("invalid geojson crs type: must be either name or link")

    elif filepath.endswith((".tif",".tiff",".geotiff")):
        pass
        # ...




                                      
        
