
import json


#################
# USER FUNCTIONS
#################

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




                                      
        
