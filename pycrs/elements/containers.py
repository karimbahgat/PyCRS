
from . import directions
from . import datums
from . import ellipsoids
    
# the final CRS object which is instantiated with all of the below and parameters
# remember to use +no_defs when outputting to proj4
# ...
class CRS:
    def __init__(self, toplevel):
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

##+proj      Projection name (see `proj -l`)
class Projection:
    proj4 = "+proj"
    ogc_wkt = "PROJECTION"
    esri_wkt = "PROJECTION"
    
    def __init__(self, value):
        self.value = value

    def to_proj4(self):
        return "+proj=%s" %self.value.proj4

    def to_ogc_wkt(self):
        return 'PROJECTION["%s"]' %self.value.ogc_wkt

    def to_esri_wkt(self):
        return 'PROJECTION["%s"]' %self.value.esri_wkt

##+datum     Datum name (see `proj -ld`)
class Datum:
    proj4 = "+datum"
    ogc_wkt = "DATUM"
    esri_wkt = "DATUM"
    
    def __init__(self, name, ellipsoid, datumshift=None):
        """
        Arguments:

        - **name**: Specific datum name instance.
        - **ellipsoid**: Ellipsoid parameter instance. 
        """
        self.name = name
        self.ellips = ellipsoid
        self.datumshift = datumshift

    def to_proj4(self):
        if self.datumshift:
            return "%s %s" % (self.ellips.to_proj4(), self.datumshift.to_proj4())
        elif isinstance(self.name, datums.Unknown):
            return "%s" % self.ellips.to_proj4()
        elif not self.name.proj4:
            # has no proj4 equivaent and is better left unspecified, so only return ellips
            return "%s" % self.ellips.to_proj4()
        else:
            return "+datum=%s %s" % (self.name.proj4, self.ellips.to_proj4())

    def to_ogc_wkt(self):
        if self.datumshift:
            return 'DATUM["%s", %s, %s]' % (self.name.ogc_wkt, self.ellips.to_ogc_wkt(), self.datumshift.to_ogc_wkt())
        else:
            return 'DATUM["%s", %s]' % (self.name.ogc_wkt, self.ellips.to_ogc_wkt())

    def to_esri_wkt(self):
        if self.datumshift:
            return 'DATUM["%s", %s, %s]' % (self.name.esri_wkt, self.ellips.to_esri_wkt(), self.datumshift.to_esri_wkt())
        else:
            return 'DATUM["%s", %s]' % (self.name.esri_wkt, self.ellips.to_esri_wkt())

    def to_geotiff(self):
        pass
        #return "GeogGeodeticDatum" 
    
##+ellps     Ellipsoid name (see `proj -le`)
class Ellipsoid:
    proj4 = "+ellps"
    ogc_wkt = "SPHEROID"
    esri_wkt = "SPHEROID"

    def __init__(self, name, semimaj_ax=None, inv_flat=None):
        """
        Arguments:

        - **name**: Specific ellipsoid name instance. 
        """
        self.name = name
        
        # get default values if not specified
        if semimaj_ax == None:
            semimaj_ax = self.name.semimaj_ax
        if inv_flat == None:
            inv_flat = self.name.inv_flat
                
        self.semimaj_ax = semimaj_ax
        self.inv_flat = inv_flat

    def to_proj4(self):
        if isinstance(self.name, ellipsoids.Unknown):
            # has no proj4 equivaent and is better left unspecified
            return "+a=%s +f=%s" % (self.semimaj_ax, self.inv_flat)
        elif not self.name.proj4:
            # has no proj4 equivaent and is better left unspecified
            return "+a=%s +f=%s" % (self.semimaj_ax, self.inv_flat)
        else:
            return "+ellps=%s +a=%s +f=%s" % (self.name.proj4, self.semimaj_ax, self.inv_flat)

    def to_ogc_wkt(self):
        return 'SPHEROID["%s", %s, %s]' % (self.name.ogc_wkt, self.semimaj_ax, self.inv_flat)
    
    def to_esri_wkt(self):
        return 'SPHEROID["%s", %s, %s]' % (self.name.esri_wkt, self.semimaj_ax, self.inv_flat)

    def to_geotiff(self):
        pass
        #return "GeogEllipsoid"

#GEOGCS
class GeogCS:
    ogc_wkt = "GEOGCS"
    esri_wkt = "GEOGCS"

    def __init__(self, name, datum, prime_mer, angunit, twin_ax=None):
        """
        Arguments:

        - **name**: Arbitrary name. 
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
        return "%s %s %s" % (self.datum.to_proj4(), self.prime_mer.to_proj4(), self.angunit.to_proj4() ) 

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

        - **name**: Arbitrary name. 
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
