
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

from . import directions

################

def find(paramname, crstype, strict=False):
    if not strict:
        paramname = paramname.lower()
    for itemname,item in globals().items():
        if itemname.startswith("_"):
            continue
        try:
            if hasattr(item, crstype):
                itemname = getattr(item, crstype)
                if not strict:
                    itemname = itemname.lower()
                if paramname == itemname:
                    return item
        except:
            pass
    else:
        return None


##################
# Ellipsoid parameters
    
##+a         Semimajor radius of the ellipsoid axis
class SemiMajorRadius:
    proj4 = "+a"    
    def __init__(self, value):
        self.value = value

    def to_proj4(self):
        return "%s=%s" % (self.proj4, self.value)

    def to_esri_wkt(self):
        return str(self.value)

    def to_ogc_wkt(self):
        return str(self.value)
    
##+b         Semiminor radius of the ellipsoid axis
class SemiMinorRadius:
    proj4 = "+b"
    def __init__(self, value):
        self.value = value

    def to_proj4(self):
        return "%s=%s" % (self.proj4, self.value)

    def to_esri_wkt(self):
        return str(self.value)

    def to_ogc_wkt(self):
        return str(self.value)

##+f         Flattening of the ellipsoid axis
class Flattening:
    proj4 = "+f"    
    def __init__(self, value):
        self.value = value

    def to_proj4(self):
        return "%s=%s" % (self.proj4, self.value)

    def to_esri_wkt(self):
        return str(self.value)

    def to_ogc_wkt(self):
        return str(self.value)

##+rf         Inverse flattening of the ellipsoid axis
class InverseFlattening:
    proj4 = "+rf"    
    def __init__(self, value):
        self.value = value

    def to_proj4(self):
        return "%s=%s" % (self.proj4, self.value)

    def to_esri_wkt(self):
        return str(self.value)

    def to_ogc_wkt(self):
        return str(self.value)
    


#################
# Other parameters

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
        return 'PARAMETER["Azimuth",%s]' % self.value

##+k         Scaling factor (old name)
##+k_0       Scaling factor (new name)
class ScalingFactor:
    proj4 = "+k"
    ogc_wkt = "scale_factor"
    
    def __init__(self, value):
        self.value = value

    def to_proj4(self):
        return "+k_0=%s" %self.value

    def to_ogc_wkt(self):
        return 'PARAMETER["scale_factor", %s]' %self.value

    def to_esri_wkt(self):
        # REALLY??
        raise Exception("Parameter %r not supported by ESRI WKT" % self)

    def to_geotiff(self):
        pass
        #return "ScaleAtNatOrigin" # or ScaleAtCenter?

##+lat_0     Latitude of origin
class LatitudeOrigin:
    proj4 = "+lat_0"
    ogc_wkt = "latitude_of_origin"
    esri_wkt = "Latitude_Of_Origin"
    
    def __init__(self, value):
        self.value = value

    def to_proj4(self):
        return "+lat_0=%s" %self.value

    def to_ogc_wkt(self):
        # SAME AS LATITUDE OF CENTER???
        return 'PARAMETER["latitude_of_origin", %s]' %self.value

    def to_esri_wkt(self):
        return 'PARAMETER["Latitude_Of_Origin", %s]' %self.value

    def to_geotiff(self):
        pass
        #return "ProjCenterLat"
    
##+lat_1     Latitude of first standard parallel
class LatitudeFirstStndParallel:
    proj4 = "+lat_1"
    ogc_wkt = "standard_parallel_1"
    esri_wkt = "Standard_Parallel_1"
    
    def __init__(self, value):
        self.value = value
        
    def to_proj4(self):
        return "+lat_1=%s" %self.value

    def to_ogc_wkt(self):
        return 'PARAMETER["standard_parallel_1", %s]' %self.value

    def to_esri_wkt(self):
        return 'PARAMETER["Standard_Parallel_1", %s]' %self.value

    def to_geotiff(self):
        pass
        #return "StdParallel1"
    
##+lat_2     Latitude of second standard parallel
class LatitudeSecondStndParallel:
    proj4 = "+lat_2"
    ogc_wkt = "standard_parallel_2"
    esri_wkt = "Standard_Parallel_2"
    
    def __init__(self, value):
        self.value = value
    
    def to_proj4(self):
        return "+lat_2=%s" %self.value

    def to_ogc_wkt(self):
        return 'PARAMETER["standard_parallel_2", %s]' %self.value

    def to_esri_wkt(self):
        return 'PARAMETER["Standard_Parallel_2", %s]' %self.value

    def to_geotiff(self):
        pass
        #return "StdParallel2"
    
##+lat_ts    Latitude of true scale
class LatitudeTrueScale:
    proj4 = "lat_ts"
    ogc_wkt = "Standard_Parallel_1"
    esri_wkt = "Standard_Parallel_1"
    
    def __init__(self, value):
        self.value = value

    def to_proj4(self):
        return "+lat_ts=%s" %self.value

    def to_ogc_wkt(self):
        return 'PARAMETER["Standard_Parallel_1", %s]' %self.value

    def to_esri_wkt(self):
        return 'PARAMETER["Standard_Parallel_1", %s]' %self.value

    def to_geotiff(self):
        pass
        #return "ProjStdParallel1"
    
##+lon_0     Central meridian
class CentralMeridian:
    proj4 = "+lon_0"
    ogc_wkt = "Central_Meridian"
    esri_wkt = "Central_Meridian"
    
    def __init__(self, value):
        self.value = value

    def to_proj4(self):
        return "+lon_0=%s" %self.value

    def to_ogc_wkt(self):
        return 'PARAMETER["Central_Meridian", %s]' %self.value

    def to_esri_wkt(self):
        return 'PARAMETER["Central_Meridian", %s]' %self.value

    def to_geotiff(self):
        pass
        #return "ProjCenterLong"

##+lonc      ? Longitude used with Oblique Mercator and possibly a few others
class LongitudeCenter:
    proj4 = "+lonc"
    ogc_wkt = "Longitude_Of_Center"
    esri_wkt = "Longitude_Of_Center"
    
    def __init__(self, value):
        self.value = value

    def to_proj4(self):
        return "+lonc=%s" %self.value

    def to_ogc_wkt(self):
        return 'PARAMETER["Longitude_Of_Center", %s]' %self.value

    def to_esri_wkt(self):
        return 'PARAMETER["Longitude_Of_Center", %s]' %self.value
    
##+lon_wrap  Center longitude to use for wrapping (see below)
    
##+over      Allow longitude output outside -180 to 180 range, disables wrapping (see below)

##+pm        Alternate prime meridian (typically a city name, see below)
class PrimeMeridian:
    proj4 = "+pm"
    ogc_wkt = "PRIMEM"
    esri_wkt = "PRIMEM"

    cities = {
        'greenwich': 0,
        'lisbon': -9.131906111111112,
        'paris': 2.337229166666667,
        'bogota': -74.08091666666667,
        'madrid': -3.687911111111111,
        'rome': 12.452333333333332,
        'bern': 7.439583333333333,
        'jakarta': 106.80771944444444,
        'ferro': -17.666666666666668,
        'brussels': 4.3679749999999995,
        'stockholm': 18.05827777777778,
        'athens': 23.716337499999998,
        'oslo': 10.722916666666666,
        }

    # based on http://proj.maptools.org/gen_parms.html
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
    
    def __init__(self, value):
        """
        The prime meridian coordinate (or city name), relative to greenwhich, where the
        longitude is considered to be 0. 

        Arguments:

        - **value**: Longitude value relative to Greenwich, or the name of one of these cities: {}. 
        """.format(', '.join(self.cities.keys()))
        self.value = value

    def get_value(self):
        value = self.value
        try:
            value = float(value)
        except:
            value = value.lower()
            if value not in self.cities:
                raise Exception("Prime meridian value {} must be a number or the name of one of these cities: {}".format(value, ', '.join(self.cities.keys())))
            value = self.cities[value]
        value = int(value) if value.is_integer() else value
        return value

    def to_proj4(self):
        return "+pm=%s" %self.get_value()

    def to_ogc_wkt(self):
        return 'PRIMEM["Greenwich", %s]' %self.get_value()

    def to_esri_wkt(self):
        return 'PRIMEM["Greenwich", %s]' %self.get_value()

##+zone     UTM zone
    
##+south     Denotes southern hemisphere UTM zone
    
##+towgs84   3 or 7 term datum transform parameters (see below)
class DatumShift:
    proj4 = "+towgs84"
    ogc_wkt = "TOWGS84"
    
    def __init__(self, value):
        """
        The WGS84 Datum shift parameter.

        Args:
        
        - **value**: A list of 3 or 7 term datum transform parameters.
        """
        self.value = value

    def to_proj4(self):
        return "+towgs84=%s" %",".join((str(val) for val in self.value))

    def to_ogc_wkt(self):
        return "TOWGS84[%s]" %",".join((str(val) for val in self.value))

    def to_esri_wkt(self):
        raise Exception("Parameter %r not supported by ESRI WKT" % self)
    
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
        return 'PARAMETER["false_easting", %s]' % self.value

    def to_esri_wkt(self):
        return 'PARAMETER["False_Easting", %s]' % self.value
    
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
        return 'PARAMETER["false_northing", %s]' % self.value

    def to_esri_wkt(self):
        return 'PARAMETER["False_Northing", %s]' % self.value

##+h       Satellite height
class SatelliteHeight:
    proj4 = "+h"
    ogc_wkt = "satellite_height"
    esri_wkt = "satellite_height"
    
    def __init__(self, value):
        self.value = value

    def to_proj4(self):
        return "+h=%s" %self.value

    def to_ogc_wkt(self):
        return 'PARAMETER["satellite_height", %s]' % self.value

    def to_esri_wkt(self):
        return 'PARAMETER["satellite_height", %s]' % self.value

##+tilt     Tilt angle
class TiltAngle:
    proj4 = "+tilt"
    
    def __init__(self, value):
        self.value = value

    def to_proj4(self):
        return "+tilt=%s" %self.value

    def to_ogc_wkt(self):
        raise Exception("Parameter not supported by OGC WKT")

    def to_esri_wkt(self):
        raise Exception("Parameter not supported by ESRI WKT")


