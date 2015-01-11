
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



##+a         Semimajor radius of the ellipsoid axis
class SemiMajorRadius:
    proj4 = "+a"    
    def __init__(self, value):
        pass

##+alpha     ? Used with Oblique Mercator and possibly a few others
class Azimuth:
    proj4 = "+alpha"
    esri_wkt = "azimuth"
    ogc_wkt = "azimuth"
    geotiff = "AzimuthAngle"
    def __init__(self, value):
        pass

##+axis      Axis orientation (new in 4.8.0)
class AxisOrientation:
    proj4 = "+axis"
    esri_wkt = None
    ogc_wkt = "AXIS"
    geotiff = None
    def __init__(self, value):
        pass

##+b         Semiminor radius of the ellipsoid axis
class SemiMinorRadius:
    proj4 = "+b"
    def __init__(self, value):
        pass
    
##+datum     Datum name (see `proj -ld`)
class DatumName:
    def __init__(self, value):
        self.value = value

    def to_proj4(self):
        return "+datum=%s" %self.value

    def to_ogc_wkt(self):
        return 'DATUM[%s]' %self.value

    def to_esri_wkt(self):
        return self.to_ogc_wkt()

    def to_geotiff(self):
        pass
        #return "GeogGeodeticDatum" 
    
##+ellps     Ellipsoid name (see `proj -le`)
class EllipsoidName:
    def __init__(self, value):
        self.value = value

    def to_proj4(self):
        return "+ellps=%s" %self.value

    def to_ogc_wkt(self):
        return 'SPHEROID[%s]' %self.value

    def to_esri_wkt(self):
        return self.to_ogc_wkt()

    def to_geotiff(self):
        pass
        #return "GeogEllipsoid" 


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
        return 'PARAMETER["latitude_of_origin", %s]' %self.value

    def to_esri_wkt(self):
        raise Exception("Paramater not supported by ESRI WKT")

    def to_geotiff(self):
        pass
        #return "ProjCenterLat"
    
##+lat_1     Latitude of first standard parallel
class LatitudeFirstStndParallel:
    proj4 = "+lat_1"
    def __init__(self, value):
        pass
    
##+lat_2     Latitude of second standard parallel
class LatitudeSecondStndParallel:
    proj4 = "+lat_2"
    def __init__(self, value):
        pass
    
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
class LongitudeSpecial:
    proj4 = "+lonc"
    def __init__(self, value):
        pass
    
##+lon_wrap  Center longitude to use for wrapping (see below)
    
##+over      Allow longitude output outside -180 to 180 range, disables wrapping (see below)

##+pm        Alternate prime meridian (typically a city name, see below)
class PrimeMeridian:
    def __init__(self, value):
        self.value = value

    def to_proj4(self):
        return "+pm=%s" %self.value

    def to_ogc_wkt(self):
        return 'PRIMEM["Greenwich", %s]' %self.value

    def to_esri_wkt(self):
        return self.to_ogc_wkt()

##+proj      Projection name (see `proj -l`)
class ProjectionName:
    def __init__(self, value):
        self.value = value

    def to_proj4(self):
        return "+proj=%s" %self.value

    def to_ogc_wkt(self):
        return 'PROJECTION["%s"]' %self.value

    def to_esri_wkt(self):
        return self.to_ogc_wkt()

    
##+south     Denotes southern hemisphere UTM zone
    
##+towgs84   3 or 7 term datum transform parameters (see below)
class DatumShift:
    def __init__(self, value):
        self.value = value

    def to_proj4(self):
        return "+towgs84=%s" %"".join((str(val) for val in self.value))

    def to_ogc_wkt(self):
        return "TOWGS84[%s]" %"".join((str(val) for val in self.value))

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
        self.value = value

    def to_proj4(self):
        return "+units=%s" %self.value

    def to_ogc_wkt(self):
        # the stuff that comes after UNITS[... # must be combined with metermultiplier in a unit class to make wkt
        return str(self.value)

    def to_esri_wkt(self):
        return self.to_ogc_wkt()

# special...
class Unit:
    def __init__(self, unittype, metermultiplier):
        self.unittype = unittype
        self.metermultiplier = metermultiplier

    def to_proj4(self):
        return "+%s +%s" %(self.unittype, self.metermultiplier)

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
        pass
    
##+y_0       False northing
class FalseEasting:
    proj4 = "+y_0"
    esri_wkt = "False_Northing"
    ogc_wkt = "false_northing"
    geotiff = "FalseNorthing"
    def __init__(self, value):
        pass


# then the final CRS object which is instantiated with all of these?
# remember to use +no_defs when outputting to proj4
# ...




