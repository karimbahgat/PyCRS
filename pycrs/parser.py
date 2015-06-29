
# parse from text strings
# possible use module: https://github.com/rockdoc/grabbag/wiki/CRS-WKT-Parser
# also note some paramter descriptions: http://www.geoapi.org/3.0/javadoc/org/opengis/referencing/doc-files/WKT.html
# and see gdal source code: http://gis.stackexchange.com/questions/129764/how-are-esri-wkt-projections-different-from-ogc-wkt-projections

from . import datums
from . import ellipsoids
from . import parameters
from . import units
from . import projections

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
    
##    proj=robin +lon_0=0 +x_0=0 +y_0=0 +ellps=WGS84 +datum=WGS84 +units=m +no_defs
##
##    PROJCS["World_Robinson",
##        GEOGCS["GCS_WGS_1984",
##            DATUM["WGS_1984",
##                SPHEROID["WGS_1984",6378137,298.257223563]],
##            PRIMEM["Greenwich",0],
##            UNIT["Degree",0.017453292519943295]],
##        PROJECTION["Robinson"],
##        PARAMETER["False_Easting",0],
##        PARAMETER["False_Northing",0],
##        PARAMETER["Central_Meridian",0],
##        UNIT["Meter",1],
##        AUTHORITY["EPSG","54030"]]

    params = []
    
    partdict = dict([part.split("=") for part in string.split()
                     if not part.startswith("+no_defs")])

    # DATUM

    # datum param is required
    if "+datum" in partdict:
        
        # get predefined datum def
        if partdict["+datum"] == "WGS84":
            datumdef = datums.WGS84()

        # ELLIPS

        # ellipse param is required
        if "+ellps" in partdict:

            # get predefined ellips def
            if partdict["+ellps"] == "WGS84":
                ellipsdef = ellipsoids.WGS84()

        else:
            raise Exception("Could not find required +ellps element")

        ## create datum and ellips param objs
        ellips = parameters.Ellipsoid(ellipsdef,
                                      semimaj_ax=partdict.get("+a"),
                                      inv_flat=partdict.get("+f"))
        datum = parameters.Datum(datumdef, ellips)

    else:
        raise Exception("Could not find required +datum element")

    # PRIME MERIDIAN

    # set default
    prime_mer = parameters.PrimeMeridian(0)

    # overwrite with user input
    if "+pm" in partdict:
        # for now only support longitude, later add name support:
##       greenwich 0dE                           
##          lisbon 9d07'54.862"W                 
##           paris 2d20'14.025"E                 
##          bogota 74d04'51.3"E                  
##          madrid 3d41'16.48"W                  
##            rome 12d27'8.4"E                   
##            bern 7d26'22.5"E                   
##         jakarta 106d48'27.79"E                
##           ferro 17d40'W                       
##        brussels 4d22'4.71"E                   
##       stockholm 18d3'29.8"E                   
##          athens 23d42'58.815"E                
##            oslo 10d43'22.5"E
        prime_mer = parameters.PrimeMeridian(partdict["+pm"])

    # ANGULAR UNIT    

    ## proj4 cannot set angular unit, so just set to default
    metmulti = parameters.MeterMultiplier(0.017453292519943295)
    unittype = parameters.UnitType(units.Degree())
    angunit = parameters.AngularUnit(unittype, metmulti)

    # GEOGCS (note, currently does not load axes)

    geogcs = parameters.GeogCS("Unknown", datum, prime_mer, angunit) #, twin_ax)

    # PROJECTION
    
    if "+proj" in partdict:

        # get predefined proj def
        if partdict["+proj"] == "robin":
            projdef = projections.Robinson()

        elif partdict["+proj"] == "longlat":
            projdef = None
            # set geogcs axis in correct order

        elif partdict["+proj"] == "latlong":
            projdef = None
            # set geogcs axis in correct order

            # ALSO SHOULDNT EXCLUDE +proj, NEED WAY TO INCLUDE IT...
            # ...

        else:
            projdef = None

    else:
        raise Exception("Could not find required +proj element")

    if projdef:

        # create proj param obj
        proj = parameters.Projection(projdef)

        # CENTRAL MERIDIAN

        if "+lon_0" in partdict:
            val = partdict["+lon_0"]
            obj = parameters.CentralMeridian(val)
            params.append(obj)

        # FALSE EASTING

        if "+x_0" in partdict:
            val = partdict["+x_0"]
            obj = parameters.FalseEasting(val)
            params.append(obj)

        # FALSE NORTHING

        if "+y_0" in partdict:
            val = partdict["+y_0"]
            obj = parameters.FalseNorthing(val)
            params.append(obj)

        # UNIT

        ## set default
        metmulti = parameters.MeterMultiplier(1.0)
        unittype = parameters.UnitType(units.Meter())

        ## override with user input
        if "+to_meter" in partdict:
            metmulti = parameters.MeterMultiplier(partdict["+to_meter"])
        if "+units" in partdict:
            if partdict["+units"] == "m":
                unittype = parameters.UnitType(units.Meter())

        ## create unitobj
        unit = parameters.Unit(unittype, metmulti)

        # PROJCS

        projcs = parameters.ProjCS("Unknown", geogcs, proj, params, unit)

        # CRS

        crs = parameters.CRS(projcs)

    else:
        crs = parameters.CRS(geogcs)

    # FINISHED

    return crs

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

def from_geotiff_parameters(**params):
    pass
