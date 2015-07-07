
# parse from text strings
# possible use module: https://github.com/rockdoc/grabbag/wiki/CRS-WKT-Parser
# also note some paramter descriptions: http://www.geoapi.org/3.0/javadoc/org/opengis/referencing/doc-files/WKT.html
# and see gdal source code: http://gis.stackexchange.com/questions/129764/how-are-esri-wkt-projections-different-from-ogc-wkt-projections
# especially: http://fossies.org/windows/misc/saga_2.1.4_x64.zip/saga_2.1.4_x64/saga_prj.dic

from . import datums
from . import ellipsoids
from . import parameters
from . import units
from . import projections
from . import webscrape

def from_epsg_code(code):
    # must go online (or look up local table) to get crs details
    code = str(code)
    proj4 = webscrape.crscode_to_string("epsg", code, "proj4")
    crs = from_proj4(proj4)
    return crs

def from_esri_code(code):
    # must go online (or look up local table) to get crs details
    code = str(code)
    proj4 = webscrape.crscode_to_string("esri", code, "proj4")
    crs = from_proj4(proj4)
    return crs

def from_sr_code(code):
    # must go online (or look up local table) to get crs details
    code = str(code)
    proj4 = webscrape.crscode_to_string("sr-org", code, "proj4")
    crs = from_proj4(proj4)
    return crs

##def from_esri_wkt(string):
##    # parse arguments into components
##    # use args to create crs
##    pass
        
def from_ogc_wkt(string):
    # remove newlines and multi spaces
    string = " ".join(string.split())
    
    # parse arguments into components
    def _consume_bracket(chars, char):
        "char must be the opening bracket"
        consumed = ""
        depth = 1
        while char and depth > 0:
            consumed += char
            char = next(chars, None)
            # update depth level
            if char == "[":
                depth += 1
            elif char == "]":
                depth -= 1
        consumed += char # consume the last closing char too
        return consumed
    
    def _consume_quote(chars, char, quotechar):
        "char and quotechar must be the opening quote char"
        consumed = ""
        # consume the first opening char
        consumed += char 
        char = next(chars, None)
        # consume inside
        while char and char != quotechar:
            consumed += char
            char = next(chars, None)
        # consume the last closing char too
        consumed += char 
        return consumed
    
    def _next_elem(chars, char):
        "char must be the first char of the text that precedes brackets"
        header = ""
        # skip until next header
        while not char.isalpha():
            char = next(chars, None)
        # first consume the element text header
        while char.isalpha():
            header += char
            char = next(chars, None)
        # skip until next brackets (in case of spaces)
        while char != "[":
            char = next(chars, None)
        # then consume the element bracket contents
        if char == "[":
            content = _consume_bracket(chars, char)
        char = next(chars, None)
        # split content into args list
        content = content[1:-1] # remove enclosing brackets
        content = _split_except(content)
        # recursively load all subelems
        for i,item in enumerate(content):
            if isinstance(item, str) and "[" in item:
                chars = (char for char in item)
                char = next(chars)
                item = _next_elem(chars, char)
                content[i] = item
        return header, content
    
    def _clean_value(string):
        string = string.strip()
        try: string = float(string)
        except: pass
        return string
    
    def _split_except(string):
        chars = (char for char in string)
        char = next(chars)
        items = []
        consumed = ""
        while char:
            # dont split on quotes, just consume it
            if char in ("'", '"'):
                consumed += _consume_quote(chars, char, char)
            # dont split inside brackets, just consume it
            elif char == "[":
                consumed += _consume_bracket(chars, char)
            # make new splititem
            elif char == ",":
                consumed = _clean_value(consumed)
                items.append(consumed)
                consumed = ""
            # consume normal char
            elif char:
                consumed += char
            # next
            char = next(chars, None)
        # append last item too
        consumed = _clean_value(consumed)
        items.append(consumed)
        return items

    # load into nested tuples and arglists
    crstuples = []
    chars = (char for char in string)
    char = next(chars)
    while char:
        header,content = _next_elem(chars, char)
        crstuples.append((header, content))
        char = next(chars, None)

    # parse into actual crs objects
    def _parse(header, content):
        if header.upper() == "PROJCS":
            # find name
            name = content[0].strip('"')
            # find geogcs elem (by running parse again)
            subheader, subcontent = content[1]
            geogcs = _parse(subheader, subcontent)
            # find projection elem
            subheader, subcontent = content[2]
            for itemname in dir(projections):
                item = getattr(projections, itemname)
                try:
                    item = item()
                    if hasattr(item, "ogc_wkt") and subcontent[0].strip('"') == item.ogc_wkt:
                        projdef = item
                        break
                except:
                    pass
            else:
                projdef = None
            proj = parameters.Projection(projdef)
            # find params
            params = []
            for part in content:
                if isinstance(part, tuple):
                    subheader,subcontent = part
                    if subheader == "PARAMETER":
                        if subcontent[0] == '"Azimuth"':
                            item = parameters.Azimuth(subcontent[1])
                            params.append(item)
                        elif subcontent[0] == '"scale_factor"':
                            item = parameters.ScalingFactor(subcontent[1])
                            params.append(item)
                        elif subcontent[0] == '"latitude_of_origin"':
                            item = parameters.LatitudeOrigin(subcontent[1])
                            params.append(item)
                        elif subcontent[0] == '"standard_parallel_1"':
                            item = parameters.LatitudeFirstStndParallel(subcontent[1])
                            params.append(item)
                        elif subcontent[0] == '"standard_parallel_2"':
                            item = parameters.LatitudeSecondStndParallel(subcontent[1])
                            params.append(item)
                        elif subcontent[0] == '"Standard_Parallel_1"':
                            item = parameters.LatitudeTrueScale(subcontent[1])
                            params.append(item)
                        elif subcontent[0] == '"Central_Meridian"':
                            item = parameters.CentralMeridian(subcontent[1])
                            params.append(item)
                        elif subcontent[0] == '"Longitude_Of_Center"':
                            item = parameters.LongitudeCenter(subcontent[1])
                            params.append(item)
                        elif subcontent[0] == '"false_easting"':
                            item = parameters.FalseEasting(subcontent[1])
                            params.append(item)
                        elif subcontent[0] == '"false_northing"':
                            item = parameters.FalseNorthing(subcontent[1])
                            params.append(item)
                        elif subcontent[0] == '"satellite_height"':
                            item = parameters.SatelliteHeight(subcontent[1])
                            params.append(item)
            # find unit
            for part in content:
                if isinstance(part, tuple):
                    subheader,subcontent = part
                    if subheader == "UNIT":
                        break
            if subcontent[0].strip('"') == "Meters":
                unittype = parameters.UnitType(units.Meter())
            elif subcontent[0].strip('"') == "degree":
                unittype = parameters.UnitType(units.Degree())
            metmult = parameters.MeterMultiplier(subcontent[1])
            unit = parameters.Unit(unittype, metmult)
            # find twin axis maybe
##            if len(content) >= 6:
##                twinax = (parameters.Axis(
##            else:
##                twinax = None
            # put it all together
            projcs = parameters.ProjCS("Unknown", geogcs, proj, params, unit) #, twinax)
            return projcs

        elif header.upper() == "GEOGCS":
            # name
            name = content[0]
            # datum
            subheader, subcontent = content[1]
            ## datum name
            for itemname in dir(datums):
                item = getattr(datums, itemname)
                try:
                    item = item()
                    if hasattr(item, "ogc_wkt") and subcontent[0].strip('"') == item.ogc_wkt:
                        datumdef = item
                        break
                except:
                    pass
            else:
                datumdef = datums.Unknown()
            ## datum ellipsoid
            subsubheader, subsubcontent = subcontent[1]
            for itemname in dir(ellipsoids):
                item = getattr(ellipsoids, itemname)
                try:
                    item = item()
                    if hasattr(item, "ogc_wkt") and subsubcontent[0].strip('"') == item.ogc_wkt:
                        ellipsdef = item
                        break
                except:
                    pass
            else:
                ellipsdef = None
            ellipsoid = parameters.Ellipsoid(ellipsdef, subsubcontent[1], subsubcontent[2])
            ## datum shift
            if len(subcontent) >= 3:
                subsubheader, subsubcontent = subcontent[2]
                datumshift = parameters.DatumShift(subsubcontent)
            else:
                datumshift = None
            ## put it all togehter
            datum = parameters.Datum(datumdef, ellipsoid, datumshift)
            # prime mer
            subheader, subcontent = content[2]
            prime_mer = parameters.PrimeMeridian(subcontent[1])
            # angunit
            subheader, subcontent = content[3]
            if subcontent[0].strip('"') == "Meters":
                unittype = parameters.UnitType(units.Meter())
            elif subcontent[0].strip('"') == "degree":
                unittype = parameters.UnitType(units.Degree())
            metmult = parameters.MeterMultiplier(subcontent[1])
            angunit = parameters.AngularUnit(unittype, metmult)
            # twin axis
            # ...
            # put it all together
            geogcs = parameters.GeogCS(name, datum, prime_mer, angunit, twin_ax=None)
            return geogcs

    # toplevel collection
    header, content in crstuples[0]
    toplevel = _parse(header, content)
    crs = parameters.CRS(toplevel)
        
    # use args to create crs
    return crs

##def from_unknown_wkt(string):
##    # detect if ogc wkt or esri wkt
##    # TIPS: esri wkt datums all use "D_" before the datum name
##    # then load with appropriate function
##    pass

def from_proj4(string):
    # parse arguments into components
    # use args to create crs

    # SLIGTHLY MESSY STILL, CLEANUP..

    params = []
    
    partdict = dict([part.split("=") for part in string.split()
                     if not part.startswith("+no_defs")])

    # INIT CODES...?
    # eg, +init=epsg code...?
    if "+init" in partdict:

        codetype, code = partdict["+init"].split(":")
        if codetype == "EPSG":
            crs = from_epsg_code(code)
            # need to get individual elements from crs
            # maybe from web...

    # DATUM

    # datum param is required
    if "+datum" in partdict:
        
        # get predefined datum def
        for itemname in dir(datums):
            item = getattr(datums, itemname)
            try:
                item = item()
                if hasattr(item, "proj4") and partdict["+datum"] == item.proj4:
                    datumdef = item
                    break
            except:
                pass

        else:
            datumdef = datums.Unknown()

    else:
        datumdef = datums.Unknown()

    # ELLIPS

    # ellipse param is required
    if "+ellps" in partdict:

        # get predefined ellips def
        for itemname in dir(ellipsoids):
            item = getattr(ellipsoids, itemname)
            try:
                item = item()
                if hasattr(item, "proj4") and partdict["+ellps"] == item.proj4:
                    ellipsdef = item
                    break
            except:
                pass

    else:
        raise Exception("Could not find required +ellps element")

    # TO WGS 84 COEFFS
    if "+towgs84" in partdict:
        coeffs = partdict["+towgs84"].split(",")
        datumshift = parameters.DatumShift(coeffs)

        # if no datum, use ellips + towgs84 params to create the correct datum
        # ...??

    # COMBINE DATUM AND ELLIPS

    ## create datum and ellips param objs
    ellips = parameters.Ellipsoid(ellipsdef,
                                  semimaj_ax=partdict.get("+a"),
                                  inv_flat=partdict.get("+f"))
    if "+datum" in partdict:
        datum = parameters.Datum(datumdef, ellips)

    elif "+towgs84" in partdict:
        datum = parameters.Datum(datumdef, ellips, datumshift)

    else:
        datum = parameters.Datum(datumdef, ellips)

    # PRIME MERIDIAN

    # set default
    prime_mer = parameters.PrimeMeridian(0)

    # overwrite with user input
    if "+pm" in partdict:
        # for now only support longitude, later add name support from below:
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
        for itemname in dir(projections):
            item = getattr(projections, itemname)
            try:
                item = item()
                if hasattr(item, "proj4") and partdict["+proj"] == item.proj4:
                    projdef = item
                    break
            except:
                pass

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

        # SCALING FACTOR
        
        if "+k_0" in partdict or "+k" in partdict:
            if "+k_0" in partdict: val = partdict["+k_0"]
            elif "+k" in partdict: val = partdict["+k"]
            obj = parameters.ScalingFactor(val)
            params.append(obj)

        # LATITUDE ORIGIN

        if "+lat_0" in partdict:
            val = partdict["+lat_0"]
            obj = parameters.LatitudeOrigin(val)
            params.append(obj)

        # LATITUDE TRUE SCALE

        if "+lat_ts" in partdict:
            val = partdict["+lat_ts"]
            obj = parameters.LatitudeTrueScale(val)
            params.append(obj)

        # LONGITUDE CENTER

        if "+lonc" in partdict:
            val = partdict["+lonc"]
            obj = parameters.LongitudeCenter(val)
            params.append(obj)

        # AZIMUTH

        if "+alpha" in partdict:
            val = partdict["+alpha"]
            obj = parameters.Azimuth(val)
            params.append(obj)

        # STD PARALLEL 1

        if "+lat1" in partdict:
            val = partdict["+lat1"]
            obj = parameters.LatitudeFirstStndParallel(val)
            params.append(obj)
            
        # STD PARALLEL 2

        if "+lat2" in partdict:
            val = partdict["+lat2"]
            obj = parameters.LatitudeSecondStndParallel(val)
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

        # SATELLITE HEIGHT
        if "+h" in partdict:
            val = partdict["+h"]
            obj = parameters.SatelliteHeight(val)
            params.append(obj)

        # TILT ANGLE
        if "+tilt" in partdict:
            val = partdict["+tilt"]
            obj = parameters.TiltAngle(val)
            params.append(obj)

        # PROJCS

        projcs = parameters.ProjCS("Unknown", geogcs, proj, params, unit)

        # CRS

        crs = parameters.CRS(projcs)

    else:
        crs = parameters.CRS(geogcs)

    # FINISHED

    return crs

##def from_ogc_urn(string):
##    # hmmm, seems like ogc urn could be anything incl online link, epsg, etc...
##    # if necessary, must go online (or lookup local table) to get details
##    # maybe test which of these and run their function?
##    # examples urn:ogc:def:crs:OGC:1.3:CRS1
##    # or with EPSG instead of OGC
##
##    # If OGC, 1.3 is pdf version, and after that is a name from list below
##    # as found in pdf: "Definition identifier URNs in OGC namespace"
##    # OGC crs definitions
##    # URN | CRS name | Definition reference
##    # urn:ogc:def:crs:OGC:1.3:CRS1 Map CS B.2 in OGC 06-042
##    # urn:ogc:def:crs:OGC:1.3:CRS84 WGS 84 longitude-latitude B.3 in OGC 06-042
##    # urn:ogc:def:crs:OGC:1.3:CRS83 NAD83 longitude-latitude B.4 in OGC 06-042
##    # urn:ogc:def:crs:OGC:1.3:CRS27 NAD27 longitude-latitude B.5 in OGC 06-042
##    # urn:ogc:def:crs:OGC:1.3:CRS88 NAVD 88 B.6 in OGC 06-042
##    # urn:ogc:def:crs:OGC:1.3:AUTO42001:99:8888 Auto universal transverse mercator B.7 in OGC 06-042
##    # urn:ogc:def:crs:OGC:1.3:AUTO42002:99:8888 Auto transverse mercator B.8 in OGC 06-042
##    # urn:ogc:def:crs:OGC:1.3:AUTO42003:99:8888 Auto orthographic B.9 in OGC 06-042
##    # urn:ogc:def:crs:OGC:1.3:AUTO42004:99:8888 Auto equirectangular B.10 in OGC 06-042
##    # urn:ogc:def:crs:OGC:1.3:AUTO42005:99 Auto Mollweide B.11 in OGC 06-042
##
##    pass

def from_unknown_text(text):
    """Detect type and load with appropriate function"""
    
    if string.startswith("urn:"):
        from_ogc_urn(string)

    elif string.startswith("+proj="):
        from_proj4(string)

    elif string.startswith("PROJCS["):
        from_unknown_wkt(string)

    elif string.startswith("EPSG:"):
        from_epsg_code(string.split(":")[1])

    elif string.startswith("ESRI:"):
        from_esri_code(string.split(":")[1])

    elif string.startswith("SR-ORG:"):
        from_sr_code(string.split(":")[1])

    else: raise Exception("Could not detect which type of crs")

##def from_geotiff_parameters(**params):
##    pass
