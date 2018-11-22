
from . import directions
from . import datums
from . import ellipsoids
    
# the final CRS object which is instantiated with all of the below and parameters
# remember to use +no_defs when outputting to proj4
# ...
class CRS:
    def __init__(self, toplevel):
        """
        The main CRS class that defines a coordinate reference system and provides access
        to all the sub-containers, sub-elements, parameters,
        and values of the reference system in a nested structure.

        Args:

        - **toplevel**: The type of reference system. Can be either a projected (arbitrary coordinates)
                        or geographic (latitude-longitude coordinates) reference system.
        """
        self.toplevel = toplevel
        
    def to_proj4(self):
        if isinstance(self.toplevel, ProjCS):
            return "%s +no_defs" % self.toplevel.to_proj4()
        elif isinstance(self.toplevel, GeogCS):
            return "+proj=longlat %s +no_defs" % self.toplevel.to_proj4()

    def to_ogc_wkt(self):
        return "%s" % self.toplevel.to_ogc_wkt()

    def to_esri_wkt(self):
        return "%s" % self.toplevel.to_esri_wkt()

#GEOGCS
class GeogCS:
    ogc_wkt = "GEOGCS"
    esri_wkt = "GEOGCS"

    def __init__(self, name, datum, prime_mer, angunit, twin_ax=None):
        """
        A geographic coordinate system where the coordinates are in the latitude-longitude space. 
        
        Arguments:

        - **name**: An arbitrary name given to this geographic coordinate system, to represent its unique
                    configuration of datum, prime meridian, angular unit, and twin axes. The actual name
                    is just for human readability, and does not actually have any implication. 
        - **datum**: A pycrs.elements.container.Datum instance, representing the shape of the earth.
        - **prime_mer**: A pycrs.elements.parameters.PrimeMeridian instance, representing the prime meridian
                    coordinate where the longitude is considered to be 0.
        - **angunit**: A pycrs.elements.parameters.AngularUnit instance, representing the angular unit in which
                    coordinates are measured.
        - **twin_ax**: A pair of pycrs.elements.directions.North/South/East/West instances, one for each axis,
                    representing the compass direction in which each axis increases. Defaults to East and North. 
        """
        self.name = name
        self.datum = datum
        self.prime_mer = prime_mer
        self.angunit = angunit
        if twin_ax == None:
            # default axes
            twin_ax = directions.East(), directions.North()
        self.twin_ax = twin_ax

    def to_proj4(self):
        # dont parse axis to proj4, because in proj4, axis only applies to the cs, ie the projcs (not the geogcs, where wkt can specify with axis)
        # also proj4 cannot specify angular units
        return "%s %s" % (self.datum.to_proj4(), self.prime_mer.to_proj4()) 

    def to_ogc_wkt(self):
        return 'GEOGCS["%s", %s, %s, %s, AXIS["Lon", %s], AXIS["Lat", %s]]' % (self.name, self.datum.to_ogc_wkt(), self.prime_mer.to_ogc_wkt(), self.angunit.to_ogc_wkt(), self.twin_ax[0].ogc_wkt, self.twin_ax[1].ogc_wkt )
    
    def to_esri_wkt(self):
        return 'GEOGCS["%s", %s, %s, %s, AXIS["Lon", %s], AXIS["Lat", %s]]' % (self.name, self.datum.to_esri_wkt(), self.prime_mer.to_esri_wkt(), self.angunit.to_esri_wkt(), self.twin_ax[0].esri_wkt, self.twin_ax[1].esri_wkt )

#PROJCS
class ProjCS:
    ogc_wkt = "PROJCS"
    esri_wkt = "PROJCS"
    
    def __init__(self, name, geogcs, proj, params, unit, twin_ax=None):
        """
        Arguments:

        - **name**: Arbitrary name of the projected coordinate system.
        - **geogcs**: A pycrs.elements.containers.GeogCS instance.
        - **proj**: A pycrs.elements.containers.Projection instance.
        - **params**: A list of custom parameters from the pycrs.elements.parameters module.
        - **unit**: A pycrs.elements.parameters.Unit instance, representing the angular unit in which
                    coordinates are measured.
        - **twin_ax**: A pair of pycrs.elements.directions.North/South/East/West instances, one for each axis,
                    representing the compass direction in which each axis increases. Defaults to East and North. 
        """
        self.name = name
        self.geogcs = geogcs
        self.proj = proj
        self.params = params
        self.unit = unit
        if twin_ax == None:
            # default axes
            twin_ax = directions.East(), directions.North()
        self.twin_ax = twin_ax

    def to_proj4(self):
        string = "%s %s " % (self.proj.to_proj4(), self.geogcs.to_proj4())
        string += " ".join(param.to_proj4() for param in self.params)
        string += " %s" % self.unit.to_proj4()
        string += " +axis=" + self.twin_ax[0].proj4 + self.twin_ax[1].proj4 + "u" # up set as default because only proj4 can set it I think...
        return string

    def to_ogc_wkt(self):
        string = 'PROJCS["%s", %s, %s, ' % (self.name, self.geogcs.to_ogc_wkt(), self.proj.to_ogc_wkt() )
        string += ", ".join(param.to_ogc_wkt() for param in self.params)
        string += ', %s' % self.unit.to_ogc_wkt()
        string += ', AXIS["X", %s], AXIS["Y", %s]]' % (self.twin_ax[0].ogc_wkt, self.twin_ax[1].ogc_wkt )
        return string
    
    def to_esri_wkt(self):
        string = 'PROJCS["%s", %s, %s, ' % (self.name, self.geogcs.to_esri_wkt(), self.proj.to_esri_wkt() )
        string += ", ".join(param.to_esri_wkt() for param in self.params)
        string += ', %s' % self.unit.to_esri_wkt()
        string += ', AXIS["X", %s], AXIS["Y", %s]]' % (self.twin_ax[0].esri_wkt, self.twin_ax[1].esri_wkt )
        return string
