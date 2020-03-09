"""
Coordinate system (CS) classes of different types.
"""

from . import directions
from . import datums
from . import ellipsoids

from .. import utils

#BASE
class CS:
    """
    Base class for all CS classes. 
    Mostly just for basic type checking. 
    """

    def to_epsg_code(self):
        """
        Looks up the EPSG code for this CS.
        
        If an exact match is found, returns the code.
        If there are multiple ambiguous matches, raise warning and return only the top result. 
        If there are no matches, returns None.
        """
        result = utils.wkt_to_epsg(self.to_esri_wkt())
        if result['exact']:
            first = result['codes'][0]
            return int(first['code'])
        
        elif len(result['codes']) > 1:
            warnings.warn('Multiple possible matches found, returning only the top result. To see all the possible matches, use instead pycrs.utils.wkt_to_epsg().')
            return None

        else:
            return None
        

#GEOGCS
class GeogCS(CS):
    """
    A geographic coordinate system where the coordinates are in the latitude-longitude space.
    
    Attributes:
    
        - **cs_type**: Type of CRS, always "Geographic".
        - **name**: An arbitrary name given to this geographic coordinate system, to represent its unique
                    configuration of datum, prime meridian, angular unit, and twin axes. The actual name
                    is just for human readability, and does not actually have any implication. 
        - **datum**: A pycrs.elements.datums.Datum instance, representing the shape of the earth.
        - **prime_mer**: A pycrs.elements.parameters.PrimeMeridian instance, representing the prime meridian
                    coordinate where the longitude is considered to be 0.
        - **angunit**: A pycrs.elements.parameters.AngularUnit instance, representing the angular unit in which
                    coordinates are measured.
        - **twin_ax**: A pair of pycrs.elements.directions.North/South/East/West instances, one for each axis,
                    representing the compass direction in which each axis increases. Defaults to East and North. 

    """
    ogc_wkt = "GEOGCS"
    esri_wkt = "GEOGCS"

    def __init__(self, name, datum, prime_mer, angunit, twin_ax=None):
        """
        Arguments:

        - **name**: An arbitrary name given to this geographic coordinate system, to represent its unique
                    configuration of datum, prime meridian, angular unit, and twin axes. The actual name
                    is just for human readability, and does not actually have any implication. 
        - **datum**: A pycrs.elements.datums.Datum instance, representing the shape of the earth.
        - **prime_mer**: A pycrs.elements.parameters.PrimeMeridian instance, representing the prime meridian
                    coordinate where the longitude is considered to be 0.
        - **angunit**: A pycrs.elements.parameters.AngularUnit instance, representing the angular unit in which
                    coordinates are measured.
        - **twin_ax**: A pair of pycrs.elements.directions.North/South/East/West instances, one for each axis,
                    representing the compass direction in which each axis increases. Defaults to East and North. 
        """
        self.cs_type = "Geographic"
        
        self.name = name
        self.datum = datum
        self.prime_mer = prime_mer
        self.angunit = angunit
        if twin_ax == None:
            # default axes
            twin_ax = directions.East(), directions.North()
        self.twin_ax = twin_ax

    def to_proj4(self, as_dict=False, toplevel=True):
        """
        Returns the CS as a proj4 formatted string or dict.

        Arguments:

        - **as_dict** (optional): If True, returns the proj4 string as a dict (defaults to False).
        - **toplevel** (optional): If True, treats this CS as the final toplevel CS and adds the necessary proj4 elements (defaults to True).
        """
        # dont parse axis to proj4, because in proj4, axis only applies to the cs, ie the projcs (not the geogcs, where wkt can specify with axis)
        # also proj4 cannot specify angular units
        if toplevel:
            string = "+proj=longlat %s %s +nodef" % (self.datum.to_proj4(), self.prime_mer.to_proj4())
        else:
            string = "%s %s" % (self.datum.to_proj4(), self.prime_mer.to_proj4())
        if as_dict:
            return dict([
                        entry.lstrip('+').split('=')
                        for entry in string.split()
                        if entry != "+no_defs"
                         ])
        else:
            return string

    def to_ogc_wkt(self):
        """
        Returns the CS as a OGC WKT formatted string.
        """
        return 'GEOGCS["%s", %s, %s, %s, AXIS["Lon", %s], AXIS["Lat", %s]]' % (self.name, self.datum.to_ogc_wkt(), self.prime_mer.to_ogc_wkt(), self.angunit.to_ogc_wkt(), self.twin_ax[0].ogc_wkt, self.twin_ax[1].ogc_wkt )
    
    def to_esri_wkt(self):
        """
        Returns the CS as a ESRI WKT formatted string.
        """
        return 'GEOGCS["%s", %s, %s, %s, AXIS["Lon", %s], AXIS["Lat", %s]]' % (self.name, self.datum.to_esri_wkt(), self.prime_mer.to_esri_wkt(), self.angunit.to_esri_wkt(), self.twin_ax[0].esri_wkt, self.twin_ax[1].esri_wkt )

#PROJCS
class ProjCS(CS):
    """
    A projected coordinate system where the coordinates are projected to euclidean x,y space.
    
    Attributes:

    - **cs_type**: Type of CRS, always "Projected".
    - **name**: Arbitrary name of the projected coordinate system.
    - **geogcs**: A pycrs.elements.cs.GeogCS instance.
    - **proj**: A pycrs.elements.projections.Projection instance.
    - **params**: A list of custom parameters from the pycrs.elements.parameters module.
    - **unit**: A pycrs.elements.parameters.Unit instance, representing the angular unit in which
                coordinates are measured.
    - **twin_ax**: A pair of pycrs.elements.directions.North/South/East/West instances, one for each axis,
                representing the compass direction in which each axis increases. Defaults to East and North. 
    """

    ogc_wkt = "PROJCS"
    esri_wkt = "PROJCS"
    
    def __init__(self, name, geogcs, proj, params, unit, twin_ax=None):
        """
        Arguments:

        - **name**: Arbitrary name of the projected coordinate system.
        - **geogcs**: A pycrs.elements.cs.GeogCS instance.
        - **proj**: A pycrs.elements.projections.Projection instance.
        - **params**: A list of custom parameters from the pycrs.elements.parameters module.
        - **unit**: A pycrs.elements.parameters.Unit instance, representing the angular unit in which
                    coordinates are measured.
        - **twin_ax**: A pair of pycrs.elements.directions.North/South/East/West instances, one for each axis,
                    representing the compass direction in which each axis increases. Defaults to East and North. 
        """
        self.cs_type = "Projected"
        self.name = name
        self.geogcs = geogcs
        self.proj = proj
        self.params = params
        self.unit = unit
        if twin_ax == None:
            # default axes
            twin_ax = directions.East(), directions.North()
        self.twin_ax = twin_ax

    def to_proj4(self, as_dict=False):
        """
        Returns the CS as a proj4 formatted string or dict.

        Arguments:

        - **as_dict** (optional): If True, returns the proj4 string as a dict (defaults to False).
        """
        string = "%s" % self.proj.to_proj4()
        string += " %s" % self.geogcs.to_proj4(toplevel=False)
        string += " " + " ".join(param.to_proj4() for param in self.params)
        string += " %s" % self.unit.to_proj4()
        string += " +axis=" + self.twin_ax[0].proj4 + self.twin_ax[1].proj4 + "u" # up set as default because only proj4 can set it I think...
        string += " +no_defs"
        
        if as_dict:
            return dict([
                        entry.lstrip('+').split('=')
                        for entry in string.split()
                        if entry != "+no_defs"
                         ])
        else:
            return string

    def to_ogc_wkt(self):
        """
        Returns the CS as a OGC WKT formatted string.
        """
        string = 'PROJCS["%s", %s, %s, ' % (self.name, self.geogcs.to_ogc_wkt(), self.proj.to_ogc_wkt() )
        string += ", ".join(param.to_ogc_wkt() for param in self.params)
        string += ', %s' % self.unit.to_ogc_wkt()
        string += ', AXIS["X", %s], AXIS["Y", %s]]' % (self.twin_ax[0].ogc_wkt, self.twin_ax[1].ogc_wkt )
        return string
    
    def to_esri_wkt(self):
        """
        Returns the CS as a ESRI WKT formatted string.
        """
        string = 'PROJCS["%s", %s, %s, ' % (self.name, self.geogcs.to_esri_wkt(), self.proj.to_esri_wkt() )
        string += ", ".join(param.to_esri_wkt() for param in self.params)
        string += ', %s' % self.unit.to_esri_wkt()
        string += ', AXIS["X", %s], AXIS["Y", %s]]' % (self.twin_ax[0].esri_wkt, self.twin_ax[1].esri_wkt )
        return string


    
