
#################
# CRS CLASSES
#################

# first classes for each crs element, from the proj4 common paramter listing
# https://trac.osgeo.org/proj/wiki/GenParms

# note also that in wkt the names of "PROJECTION", "DATUM", and "SPHEROID"
# matter and seem to be interpreted and computed upon, ie they carry meaning
# that is commonly understood by programs, so is not explicit in the crs specification.

# the paramters below simply modify certain aspects of the proj/datum/spheroids

# note that the names in wkt of "PROJCS" and "GEOGCS" seem to be purely
# for identifying and branding and can be changed at will.
# they do however act as shortcuts, so that proj4 can use +init=... to load
# everything automatically

# some of these names imply certain combinations of datum and spheroid and paramters.
# so in proj4 one simply needs to give that name, but in wkt one needs to spell it all out.

# +unit and +to_metre are what makes up 'UNIT["Meter",1.0]'

from . import directions


# ONLY PURE VALUES INSIDE ELLIPSOID...

##+a         Semimajor radius of the ellipsoid axis
class SemiMajorRadius:
    proj4 = "+a"    
    def __init__(self, value):
        pass

##+b         Semiminor radius of the ellipsoid axis
class SemiMinorRadius:
    proj4 = "+b"
    def __init__(self, value):
        pass
    


#################

##+alpha     ? Used with Oblique Mercator and possibly a few others
class Azimuth:
    proj4 = "+alpha"
    esri_wkt = "azimuth"
    ogc_wkt = "azimuth"
    geotiff = "AzimuthAngle"
    def __init__(self, value):
        self.value = value

    def to_proj4(self):
        return "+alpha=%s" % self.value

    def to_ogc_wkt(self):
        return 'PARAMETER["Azimuth",%s]' % self.value

    def to_esri_wkt(self):
        return self.to_ogc_wkt()    
    
##+datum     Datum name (see `proj -ld`)
class Datum:
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
        else:
            return "+datum=%s %s" % (self.name.proj4, self.ellips.to_proj4())

    def to_ogc_wkt(self):
        if self.datumshift:
            return 'DATUM["%s", %s, %s]' % (self.name.ogc_wkt, self.ellips.to_ogc_wkt(), self.datumshift.to_ogc_wkt())
        else:
            return 'DATUM["%s", %s]' % (self.name.ogc_wkt, self.ellips.to_ogc_wkt())

    def to_esri_wkt(self):
        return self.to_ogc_wkt()

    def to_geotiff(self):
        pass
        #return "GeogGeodeticDatum" 
    
##+ellps     Ellipsoid name (see `proj -le`)
class Ellipsoid:
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
        return "+ellps=%s +a=%s +f=%s" % (self.name.proj4, self.semimaj_ax, self.inv_flat)

    def to_ogc_wkt(self):
        return 'SPHEROID["%s", %s, %s]' % (self.name.ogc_wkt, self.semimaj_ax, self.inv_flat)
    
    def to_esri_wkt(self):
        return self.to_ogc_wkt()

    def to_geotiff(self):
        pass
        #return "GeogEllipsoid"

#GEOGCS
class GeogCS:
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
        return "%s %s %s" % (self.datum.to_proj4(), self.prime_mer.to_proj4(), self.angunit.to_proj4() ) #+axis= AND #, self.twin_ax[0].proj4, self.twin_ax[1].proj4 )

    def to_ogc_wkt(self):
        return 'GEOGCS["%s", %s, %s, %s, AXIS["Lon", %s], AXIS["Lat", %s]]' % (self.name, self.datum.to_ogc_wkt(), self.prime_mer.to_ogc_wkt(), self.angunit.to_ogc_wkt(), self.twin_ax[0].ogc_wkt, self.twin_ax[1].ogc_wkt )
    
    def to_esri_wkt(self):
        return self.to_ogc_wkt()

#PROJCS
class ProjCS:
    def __init__(self, name, geogcs, proj, params, unit, twin_ax=None):
        """
        Arguments:

        - **name**: Arbitrary name. 
        """
        self.name = name
        self.geogcs = geogcs
        self.proj = proj
        self.params = params
        if twin_ax == None:
            # default axes
            twin_ax = directions.East(), directions.North()
        self.twin_ax = twin_ax

    def to_proj4(self):
        string = "%s %s " % (self.proj.to_proj4(), self.geogcs.to_proj4())
        string += " ".join(param.to_proj4() for param in self.params)
        # in proj4, axis only applies to the cs, ie the projcs (not the geogcs, where wkt can specify with axis)
        string += " +axis=" + self.twin_ax[0].proj4 + self.twin_ax[1].proj4 + "u" # up set as default because only proj4 can set it I think...
        return string

    def to_ogc_wkt(self):
        string = 'PROJCS["%s", %s, %s, ' % (self.name, self.geogcs.to_ogc_wkt(), self.proj.to_ogc_wkt() )
        string += ", ".join(param.to_ogc_wkt() for param in self.params)
        string += ', AXIS["X", %s], AXIS["Y", %s]]' % (self.twin_ax[0].ogc_wkt, self.twin_ax[1].ogc_wkt )
        return string
    
    def to_esri_wkt(self):
        return self.to_ogc_wkt()

##+k         Scaling factor (old name)
##+k_0       Scaling factor (new name)
class ScalingFactor:
    def __init__(self, value):
        self.value = value

    def to_proj4(self):
        return "+k_0=%s" %self.value

    def to_ogc_wkt(self):
        return 'PARAMETER["scale_factor", %s]' %self.value

    def to_esri_wkt(self):
        raise Exception("Paramater not supported by ESRI WKT")

    def to_geotiff(self):
        pass
        #return "ScaleAtNatOrigin" # or ScaleAtCenter?

##+lat_0     Latitude of origin
class LatitudeOrigin:
    def __init__(self, value):
        self.value = value

    def to_proj4(self):
        return "+lat_0=%s" %self.value

    def to_ogc_wkt(self):
        # SAME AS LATITUDE OF CENTER???
        return 'PARAMETER["latitude_of_origin", %s]' %self.value

    def to_esri_wkt(self):
        raise Exception("Paramater not supported by ESRI WKT")

    def to_geotiff(self):
        pass
        #return "ProjCenterLat"
    
##+lat_1     Latitude of first standard parallel
class LatitudeFirstStndParallel:
    def __init__(self, value):
        self.value = value
        
    def to_proj4(self):
        return "+lat_1=%s" %self.value

    def to_ogc_wkt(self):
        return 'PARAMETER["standard_parallel_1", %s]' %self.value

    def to_esri_wkt(self):
        return self.to_ogc_wkt()

    def to_geotiff(self):
        pass
        #return "StdParallel1"
    
##+lat_2     Latitude of second standard parallel
class LatitudeSecondStndParallel:
    def __init__(self, value):
        self.value = value
    
    def to_proj4(self):
        return "+lat_2=%s" %self.value

    def to_ogc_wkt(self):
        return 'PARAMETER["standard_parallel_2", %s]' %self.value

    def to_esri_wkt(self):
        return self.to_ogc_wkt()

    def to_geotiff(self):
        pass
        #return "StdParallel2"
    
##+lat_ts    Latitude of true scale
class LatitudeTrueScale:
    def __init__(self, value):
        self.value = value

    def to_proj4(self):
        return "+lat_ts=%s" %self.value

    def to_ogc_wkt(self):
        return 'PARAMETER["Standard_Parallel_1", %s]' %self.value

    def to_esri_wkt(self):
        return self.to_ogc_wkt()

    def to_geotiff(self):
        pass
        #return "ProjStdParallel1"
    
##+lon_0     Central meridian
class CentralMeridian:
    def __init__(self, value):
        self.value = value

    def to_proj4(self):
        return "+lon_0=%s" %self.value

    def to_ogc_wkt(self):
        return 'PARAMETER["Central_Meridian", %s]' %self.value

    def to_esri_wkt(self):
        return self.to_ogc_wkt()

    def to_geotiff(self):
        pass
        #return "ProjCenterLong"

##+lonc      ? Longitude used with Oblique Mercator and possibly a few others
class LongitudeCenter:
    proj4 = "+lonc"
    def __init__(self, value):
        self.value = value

    def to_proj4(self):
        return "+lonc=%s" %self.value

    def to_ogc_wkt(self):
        return 'PARAMETER["Longitude_Of_Center", %s]' %self.value

    def to_esri_wkt(self):
        return self.to_ogc_wkt()
    
##+lon_wrap  Center longitude to use for wrapping (see below)
    
##+over      Allow longitude output outside -180 to 180 range, disables wrapping (see below)

##+pm        Alternate prime meridian (typically a city name, see below)
class PrimeMeridian:
    def __init__(self, value):
        """
        Arguments:

        - **value**: Longitude value relative to Greenwich. 
        """
        self.value = value

    def to_proj4(self):
        return "+pm=%s" %self.value

    def to_ogc_wkt(self):
        return 'PRIMEM["Greenwich", %s]' %self.value

    def to_esri_wkt(self):
        return self.to_ogc_wkt()

##+proj      Projection name (see `proj -l`)
class Projection:
    def __init__(self, value):
        self.value = value

    def to_proj4(self):
        return "+proj=%s" %self.value.proj4

    def to_ogc_wkt(self):
        return 'PROJECTION["%s"]' %self.value.ogc_wkt

    def to_esri_wkt(self):
        return self.to_ogc_wkt()

##+zone     UTM zone
    
##+south     Denotes southern hemisphere UTM zone
    
##+towgs84   3 or 7 term datum transform parameters (see below)
class DatumShift:
    def __init__(self, value):
        self.value = value

    def to_proj4(self):
        return "+towgs84=%s" %",".join((str(val) for val in self.value))

    def to_ogc_wkt(self):
        return "TOWGS84[%s]" %",".join((str(val) for val in self.value))

    def to_esri_wkt(self):
        raise Exception("Paramater not supported by ESRI WKT")
    
##+to_meter  Multiplier to convert map units to 1.0m
class MeterMultiplier:
    def __init__(self, value):
        self.value = value

    def to_proj4(self):
        return "+to_meter=%s" %self.value

    def to_ogc_wkt(self):
        # the stuff that comes after UNITS["meter", ... # must be combined with unittype in a unit class to make wkt
        return str(self.value)

    def to_esri_wkt(self):
        return self.to_ogc_wkt()

##+units     meters, US survey feet, etc.
class UnitType:
    def __init__(self, value):
        """
        Arguments:

        - **value**: A specific unit type instance, eg Meter(). 
        """
        self.value = value

    def to_proj4(self):
        return "+units=%s" %self.value.proj4

    def to_ogc_wkt(self):
        # the stuff that comes after UNITS[... # must be combined with metermultiplier in a unit class to make wkt
        return str(self.value.ogc_wkt)

    def to_esri_wkt(self):
        return self.to_ogc_wkt()

# special...
class Unit:
    def __init__(self, unittype, metermultiplier):
        self.unittype = unittype
        self.metermultiplier = metermultiplier

    def to_proj4(self):
        return "%s %s" %(self.unittype.to_proj4(), self.metermultiplier.to_proj4())

    def to_ogc_wkt(self):
        return 'UNIT["%s", %s]' %(self.unittype.to_ogc_wkt(), self.metermultiplier.to_ogc_wkt())

    def to_esri_wkt(self):
        return self.to_ogc_wkt()

# angular unit
class AngularUnit:
    def __init__(self, unittype, metermultiplier):
        self.unittype = unittype
        self.metermultiplier = metermultiplier

    def to_proj4(self):
        # cannot be specified in proj4, so just return nothing
        return ""

    def to_ogc_wkt(self):
        return 'UNIT["%s", %s]' %(self.unittype.to_ogc_wkt(), self.metermultiplier.to_ogc_wkt())

    def to_esri_wkt(self):
        return self.to_ogc_wkt()
    
##+x_0       False easting
class FalseEasting:
    proj4 = "+x_0"
    esri_wkt = "False_Easting"
    ogc_wkt = "false_easting"
    geotiff = "FalseEasting"
    
    def __init__(self, value):
        self.value = value

    def to_proj4(self):
        return "+x_0=%s" %self.value

    def to_ogc_wkt(self):
        # the stuff that comes after UNITS[... # must be combined with metermultiplier in a unit class to make wkt
        return 'PARAMETER["false_easting", %s]' % self.value

    def to_esri_wkt(self):
        return self.to_ogc_wkt()
    
##+y_0       False northing
class FalseNorthing:
    proj4 = "+y_0"
    esri_wkt = "False_Northing"
    ogc_wkt = "false_northing"
    geotiff = "FalseNorthing"
    
    def __init__(self, value):
        self.value = value

    def to_proj4(self):
        return "+y_0=%s" %self.value

    def to_ogc_wkt(self):
        # the stuff that comes after UNITS[... # must be combined with metermultiplier in a unit class to make wkt
        return 'PARAMETER["false_northing", %s]' % self.value

    def to_esri_wkt(self):
        return self.to_ogc_wkt()
    
# then the final CRS object which is instantiated with all of these?
# remember to use +no_defs when outputting to proj4
# ...
class CRS:
    def __init__(self, toplevel):
        self.toplevel = toplevel
        
    def to_proj4(self):
        return "%s +no_defs" % self.toplevel.to_proj4()

    def to_ogc_wkt(self):
        return "%s" % self.toplevel.to_ogc_wkt()

    def to_esri_wkt(self):
        return self.to_ogc_wkt()


