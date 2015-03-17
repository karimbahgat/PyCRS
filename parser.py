
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
    # examples urn:ogc:def:crs:OGC:1.3:CRS1
    # or with EPSG instead of OGC

    # If OGC, 1.3 is pdf version, and after that is a name from list below
    # as found in pdf: "Definition identifier URNs in OGC namespace"
    # OGC crs definitions
    # URN | CRS name | Definition reference
    # urn:ogc:def:crs:OGC:1.3:CRS1 Map CS B.2 in OGC 06-042
    # urn:ogc:def:crs:OGC:1.3:CRS84 WGS 84 longitude-latitude B.3 in OGC 06-042
    # urn:ogc:def:crs:OGC:1.3:CRS83 NAD83 longitude-latitude B.4 in OGC 06-042
    # urn:ogc:def:crs:OGC:1.3:CRS27 NAD27 longitude-latitude B.5 in OGC 06-042
    # urn:ogc:def:crs:OGC:1.3:CRS88 NAVD 88 B.6 in OGC 06-042
    # urn:ogc:def:crs:OGC:1.3:AUTO42001:99:8888 Auto universal transverse mercator B.7 in OGC 06-042
    # urn:ogc:def:crs:OGC:1.3:AUTO42002:99:8888 Auto transverse mercator B.8 in OGC 06-042
    # urn:ogc:def:crs:OGC:1.3:AUTO42003:99:8888 Auto orthographic B.9 in OGC 06-042
    # urn:ogc:def:crs:OGC:1.3:AUTO42004:99:8888 Auto equirectangular B.10 in OGC 06-042
    # urn:ogc:def:crs:OGC:1.3:AUTO42005:99 Auto Mollweide B.11 in OGC 06-042

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
