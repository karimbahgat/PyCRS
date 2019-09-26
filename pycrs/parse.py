"""
The main module containing functions for parsing text strings into crs objects.
"""

# possible use module: https://github.com/rockdoc/grabbag/wiki/CRS-WKT-Parser
# also note some paramter descriptions: http://www.geoapi.org/3.0/javadoc/org/opengis/referencing/doc-files/WKT.html
# and see gdal source code: http://gis.stackexchange.com/questions/129764/how-are-esri-wkt-projections-different-from-ogc-wkt-projections
# especially: http://fossies.org/windows/misc/saga_2.1.4_x64.zip/saga_2.1.4_x64/saga_prj.dic
# also: http://saga.sourcearchive.com/documentation/2.0.7plus-pdfsg-2/crs__base_8cpp_source.html

from .elements import datums
from .elements import ellipsoids
from .elements import parameters
from .elements import cs as containers
from .elements import units
from .elements import projections
from . import utils

import warnings


class FormatError(Exception):
    pass


def from_epsg_code(code):
    """
    Load crs object from epsg code, via spatialreference.org.
    Parses based on the proj4 representation.

    Arguments:

    - *code*: The EPSG code as an integer.

    Returns:

    - A CS instance of the indicated type. 
    """
    # must go online (or look up local table) to get crs details
    code = str(code)
    proj4 = utils.crscode_to_string("epsg", code, "proj4")
    crs = from_proj4(proj4)
    return crs

def from_esri_code(code):
    """
    Load crs object from esri code, via spatialreference.org.
    Parses based on the proj4 representation.

    Arguments:

    - *code*: The ESRI code as an integer.

    Returns:

    - A CS instance of the indicated type. 
    """
    # must go online (or look up local table) to get crs details
    code = str(code)
    proj4 = utils.crscode_to_string("esri", code, "proj4")
    crs = from_proj4(proj4)
    return crs

def from_sr_code(code):
    """
    Load crs object from sr-org code, via spatialreference.org.
    Parses based on the proj4 representation.

    Arguments:

    - *code*: The SR-ORG code as an integer.

    Returns:

    - A CS instance of the indicated type. 
    """
    # must go online (or look up local table) to get crs details
    code = str(code)
    proj4 = utils.crscode_to_string("sr-org", code, "proj4")
    crs = from_proj4(proj4)
    return crs

def from_ogc_wkt(string, strict=False):
    """
    Parse crs as ogc wkt formatted string and return the resulting crs object.

    Arguments:

    - *string*: The OGC WKT representation as a string.
    - *strict* (optional): When True, the parser is strict about names having to match
        exactly with upper and lowercases. Default is not strict (False).

    Returns:

    - A CS instance of the indicated type. 
    """
    # parse arguments into components
    # use args to create crs
    return _from_wkt(string, "ogc", strict)

def from_esri_wkt(string, strict=False):
    """
    Parse crs as esri wkt formatted string and return the resulting crs object.

    Arguments:

    - *string*: The ESRI WKT representation as a string.
    - *strict* (optional): When True, the parser is strict about names having to match
        exactly with upper and lowercases. Default is not strict (False).

    Returns:

    - A CS instance of the indicated type. 
    """
    # parse arguments into components
    # use args to create crs
    return _from_wkt(string, "esri", strict)

def from_unknown_wkt(string, strict=False):
    """
    Given an unknown wkt string, detect if uses ogc or esri flavor, and parse the crs accordingly.

    Arguments:

    - *string*: The unknown WKT representation as a string.
    - *strict* (optional): When True, the parser is strict about names having to match
        exactly with upper and lowercases. Default is not strict (False).

    Returns:
    - A CS instance of the indicated type. 
    """
    # parse arguments into components
    # use args to create crs
    return _from_wkt(string, None, strict)

def _from_wkt(string, wkttype=None, strict=False):
    """
    Internal method for parsing wkt, with minor differences depending on ogc or esri style.

    Arguments:

    - *string*: The OGC or ESRI WKT representation as a string.
    - *wkttype* (optional): How to parse the WKT string, as either 'ogc', 'esri', or None. If None, tries to autodetect the wkt type before parsing (default). 
    - *strict* (optional): When True, the parser is strict about names having to match
        exactly with upper and lowercases. Default is not strict (False).

    Returns:

    - A CS instance of the indicated type. 
    """
    # TODO
    # - Make function for finding next elemt by name, instead of knowing its arg index position
    # - Maybe verify elem arg name

    # make sure valid wkttype
    if wkttype: wkttype = wkttype.lower()
    assert wkttype in ("ogc","esri",None)
    
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
        "split the string on every comma, except not while inside quotes or square brackets"
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
            # new splitchar found, add what has been consumed so far as an item, reset, and start consuming until next splitchar
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

    # autodetect wkttype if not specified
    if not wkttype:
        topheader,topcontent = crstuples[0]
        if topheader == "PROJCS":
            geogcsheader,geogcscontent = topcontent[1]
        elif topheader == "GEOGCS":
            geogcsheader,geogcscontent = topheader,topcontent

        # datum elem should be second under geogcs
        datumheader, datumcontent = geogcscontent[1]
        datumname = datumcontent[0].upper().strip('"')
        
        # esri wkt datums all use "D_" before the datum name
        if datumname.startswith("D_"):
            wkttype = "esri"
        else:
            wkttype = "ogc"

    # parse into actual crs objects
    def _parse_top(header, content):
        "procedure for parsing the toplevel crs element and all its children"
        if header.upper() == "PROJCS":
            
            # find name
            csname = content[0].strip('"')
            
            # find geogcs elem (by running parse again)
            subheader, subcontent = content[1]
            geogcs = _parse_top(subheader, subcontent)
            
            # find projection elem
            for part in content:
                if isinstance(part, tuple):
                    subheader,subcontent = part
                    if subheader == "PROJECTION":
                        break
            projname = subcontent[0].strip('"')
            projclass = projections.find(projname, "%s_wkt" % wkttype, strict)
            if projclass:
                proj = projclass()
            else:
                raise NotImplementedError("Unsupported projection: The specified projection name %r could not be found in the list of supported projections" % projname)
            
            # find params
            params = []
            for part in content:
                if isinstance(part, tuple):
                    subheader,subcontent = part
                    if subheader == "PARAMETER":
                        name, value = subcontent[0].strip('"'), subcontent[1]
                        itemclass = parameters.find(name, "%s_wkt" % wkttype, strict)
                        if itemclass:
                            item = itemclass(value)
                            params.append(item)
                            
            # find unit
            for part in content:
                if isinstance(part, tuple):
                    subheader,subcontent = part
                    if subheader == "UNIT":
                        break
            unitname,value = subcontent[0].strip('"'), subcontent[1]
            unitclass = units.find(unitname, "%s_wkt" % wkttype, strict)
            if unitclass:
                unit = unitclass()
            else:
                unit = units.Unknown()

            unit.unitmultiplier.value = value # override default multiplier
            linunit = unit
            
            # find twin axis maybe
##            if len(content) >= 6:
##                twinax = (parameters.Axis(
##            else:
##                twinax = None
            
            # put it all together
            projcs = containers.ProjCS(csname, geogcs, proj, params, linunit) #, twinax)
            return projcs

        elif header.upper() == "GEOGCS":
            # name
            csname = content[0].strip('"')
            
            # datum
            subheader, subcontent = content[1]
            
            ## datum name
            datumname = subcontent[0].strip('"')
            datumclass = datums.find(datumname, "%s_wkt" % wkttype, strict)
            if datumclass:
                datum = datumclass()
            else:
                datum = datums.Unknown()
                
            ## datum ellipsoid
            subsubheader, subsubcontent = subcontent[1]
            ellipsname = subsubcontent[0].strip('"')
            ellipsclass = ellipsoids.find(ellipsname, "%s_wkt" % wkttype, strict)
            if ellipsclass:
                ellipsoid = ellipsclass()
            else:
                if datum.ellips:
                    ellipsoid = datum.ellips
                elif not datum.ellips:
                    ellipsoid = ellipsoids.Unknown()

            ellipsoid.semimaj_ax = parameters.SemiMajorRadius(subsubcontent[1])
            if subsubcontent[2] == 0:
                # WKT falsely sets inverse flattening to 0 for spheroids
                # but actually it cannot be 0, it is the flattening that is 0
                ellipsoid.flat = parameters.Flattening(subsubcontent[2])
            else:
                ellipsoid.inv_flat = parameters.InverseFlattening(subsubcontent[2])

            ## datum shift
            if wkttype == "ogc":
                for subsubheader,subsubcontent in subcontent[1:]:
                    if subsubheader == "TOWGS84":
                        datumshift = parameters.DatumShift(subsubcontent)
                        break
                else:
                    datumshift = None
            elif wkttype == "esri":
                # not used in esri wkt
                datumshift = None
                
            ## put it all togehter
            datum.ellips = ellipsoid
            datum.datumshift = datumshift
            
            # prime mer
            subheader, subcontent = content[2]
            prime_mer = parameters.PrimeMeridian(subcontent[1])
            
            # angunit
            subheader, subcontent = content[3]
            unitname,value = subcontent[0].strip('"'), subcontent[1]
            unitclass = units.find(unitname, "%s_wkt" % wkttype, strict)
            if unitclass:
                unit = unitclass()
            else:
                unit = units.Unknown()
            unit.unitmultiplier.value = value # override default multiplier
            angunit = unit
            
            # twin axis
            # ...
            
            # put it all together
            geogcs = containers.GeogCS(csname, datum, prime_mer, angunit, twin_ax=None)
            return geogcs

    # toplevel collection
    header, content = crstuples[0]
    crs = _parse_top(header, content)
        
    # use args to create crs
    return crs

def from_proj4(proj4, strict=False):
    """
    Parse crs as proj4 formatted string or dict and return the resulting crs object.

    Arguments:

    - *proj4*: The proj4 representation as a string or dict.
    - *strict* (optional): When True, the parser is strict about names having to match
        exactly with upper and lowercases. Default is not strict (False).

    Returns:

    - A CS instance of the indicated type. 
    """
    # parse arguments into components
    # use args to create crs

    # TODO: SLIGTHLY MESSY STILL, CLEANUP..

    params = []

    if isinstance(proj4, dict):
        # add leading + sign as expected below, proj4 dicts do not have that
        partdict = dict([('+'+k,v) for k,v in proj4.items()])
    else: 
        partdict = dict([part.split("=") for part in proj4.split()
                         if len(part.split("=")) == 2 ])

    # INIT CODES
    # eg, +init=EPSG:1234
    if "+init" in partdict:

        # first, get the default proj4 string of the +init code
        codetype, code = partdict["+init"].split(":")
        codetype = codetype.upper()
        if codetype == "EPSG":
            initproj4 = utils.crscode_to_string("epsg", code, "proj4")
        elif codetype == "ESRI":
            initproj4 = utils.crscode_to_string("esri", code, "proj4")

        # make the default into param dict
        initpartdict = dict([part.split("=") for part in initproj4.split()
                             if len(part.split("=")) == 2 ])

        # override the default with any custom params specified along with the +init code
        initpartdict.update(partdict)

        # rerun from_proj4() again on the derived proj4 params as if it was not made with the +init code
        del initpartdict["+init"]
        string = " ".join("%s=%s" % (key,val) for key,val in initpartdict.items())
        return from_proj4(string)

    # DATUM

    # datum param is required
    if "+datum" in partdict:
        
        # get predefined datum def
        datumname = partdict["+datum"]
        datumclass = datums.find(datumname, "proj4", strict)
        if datumclass:
            datum = datumclass()
        else:
            datum = datums.Unknown()

    else:
        datum = datums.Unknown()

    # ELLIPS

    # ellipse param is required
    ellips = None
    if "+ellps" in partdict:

        # get predefined ellips def
        ellipsname = partdict["+ellps"]
        ellipsclass = ellipsoids.find(ellipsname, "proj4", strict)
        if ellipsclass:
            ellips = ellipsclass()
        else:
            warnings.warn('Ellipsoid "{}" could not be found in pycrs.ellipsoids, looking for manual specification instead.'.format(ellipsname))

    if not ellips:
        if datum.ellips:
            ellips = datum.ellips
        elif not datum.ellips:
            ellips = ellipsoids.Unknown()

    # TO WGS 84 COEFFS
    if "+towgs84" in partdict:
        coeffs = partdict["+towgs84"].split(",")
        datumshift = parameters.DatumShift(coeffs)

        # TODO: if no datum, use ellips + towgs84 params to create the correct datum
        # ...??

    # COMBINE DATUM AND ELLIPS

    ## create datum and ellips param objs

    # +ellps loads all the required ellipsoid parameters
    # here we set or overwrite the parameters manually
    if "+a" in partdict:
        # semimajor radius
        ellips.semimaj_ax = parameters.SemiMajorRadius(partdict["+a"])        

    if "+b" in partdict:
        # semiminor radius
        ellips.semimin_ax = parameters.SemiMinorRadius(partdict["+b"])

    if "+f" in partdict:
        # flattening
        ellips.flat = parameters.Flattening(partdict["+f"])

    if "+rf" in partdict:
        # inverse flattening
        ellips.inv_flat = parameters.InverseFlattening(partdict["+rf"])

    # check that ellipsoid is sufficiently defined
    if ellips.semimaj_ax and ellips.semimin_ax:
        # +a (semimajor radius) and +b (semiminor radius) is enough and can be used to calculate flattening
        # see https://en.wikipedia.org/wiki/Flattening
        pass
    elif ellips.semimaj_ax and ellips.inv_flat:
        # alternatively, it is okay with if +a (semimajor) and +f (flattening) are specified
        pass
    elif ellips.semimaj_ax and ellips.flat:
        # alternatively, semimajor and +rf is also acceptable (the reciprocal/inverse of +f)
        pass
    elif isinstance(ellips, ellipsoids.Unknown):
        raise Exception("Ellipsoid '{}' could not be found in pycrs.ellipsoids, and the format string did not contain the alternative manual specification of the +a with +b or +f/+rf elements".format(ellipsname))
    else:
        raise FormatError("The format string is missing the required +ellps element, or the alternative manual specification of the +a with +b or +f/+rf elements: \n\t %s" % partdict)
    
    if "+datum" in partdict:
        datum.ellips = ellips

    elif "+towgs84" in partdict:
        datum.ellips = ellips
        datum.datumshift = datumshift

    else:
        datum.ellips = ellips

    # PRIME MERIDIAN

    # set default
    prime_mer = parameters.PrimeMeridian(0)

    # overwrite with user input
    if "+pm" in partdict:
        prime_mer = parameters.PrimeMeridian(partdict["+pm"])

    # ANGULAR UNIT    

    ## proj4 cannot set angular unit, so just set to default
    angunit = units.Degree() 

    # GEOGCS (note, currently does not load axes)

    geogcs = containers.GeogCS("Unknown", datum, prime_mer, angunit) #, twin_ax)

    # PROJECTION
    
    if "+proj" in partdict:

        # get predefined proj def
        projname = partdict["+proj"]
        projclass = projections.find(projname, "proj4", strict)
        if projclass:
            proj = projclass()
        elif projname == "longlat":
            # proj4 special case, longlat as projection name means unprojected geogcs
            proj = None
        else:
            raise NotImplementedError("Unsupported projection: The specified projection name %r could not be found in the list of supported projections" % projname)

    else:
        raise FormatError("The format string is missing the required +proj element")

    if proj:

        # Because proj4 has no element hierarchy, using automatic element find() would
        # ...would not be very effective, as that would need a try-fail approach for each
        # ...element type (parameter, projection, datum, ellipsoid, unit).
        # ...Instead load each element individually.

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

        if "+lat_1" in partdict:
            val = partdict["+lat_1"]
            obj = parameters.LatitudeFirstStndParallel(val)
            params.append(obj)
            
        # STD PARALLEL 2

        if "+lat_2" in partdict:
            val = partdict["+lat_2"]
            obj = parameters.LatitudeSecondStndParallel(val)
            params.append(obj)
            
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

        # UNIT

        # get values
        if "+units" in partdict:
            # unit name takes precedence over to_meter
            unitname = partdict["+units"]
            unitclass = units.find(unitname, "proj4", strict)
            if unitclass:
                unit = unitclass() # takes meter multiplier from name, ignoring any custom meter multiplier
            else:
                raise FormatError("The specified unit name %r does not appear to be a valid unit name" % unitname)
        elif "+to_meter" in partdict:
            # no unit name specified, only to_meter conversion factor
            unit = units.Unknown()
            unit.unitmultiplier.value = partdict["+to_meter"]
        else:
            # if nothing specified, defaults to meter
            unit = units.Meter()

        # PROJCS

        projcs = containers.ProjCS("Unknown", geogcs, proj, params, unit)
        return projcs

    else:
        # means projdef was None, ie unprojected longlat geogcs
        return geogcs


##def from_ogc_urn(string, strict=False):
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


def from_unknown_text(text, strict=False):
    """
    Detect crs string format and parse into crs object with appropriate function.

    Arguments:

    - *text*: The crs text representation of unknown type. 
    - *strict* (optional): When True, the parser is strict about names having to match
        exactly with upper and lowercases. Default is not strict (False).

    Returns:

    - CRS object.
    """

    if text.startswith("+"):
        crs = from_proj4(text, strict)

    elif text.startswith(("PROJCS[","GEOGCS[")):
        crs = from_unknown_wkt(text, strict)

    #elif text.startswith("urn:"):
    #    crs = from_ogc_urn(text, strict)

    elif text.startswith("EPSG:"):
        crs = from_epsg_code(text.split(":")[1])

    elif text.startswith("ESRI:"):
        crs = from_esri_code(text.split(":")[1])

    elif text.startswith("SR-ORG:"):
        crs = from_sr_code(text.split(":")[1])

    else: raise FormatError("Could not auto-detect the type of crs format, make sure it is one of the supported formats")
    
    return crs


##def from_geotiff_parameters(**params):
##    pass



