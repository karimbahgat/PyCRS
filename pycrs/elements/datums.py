"""
Named datum classes that can be created or parsed. 
"""

from . import ellipsoids
from . import parameters


def find(datumname, crstype, strict=False):
    """
    Search for a datum name located in this module.

    Arguments:

    - **datumname**: The datum name to search for.
    - **crstype**: Which CRS naming convention to search (different
        CRS formats have different names for the same datum).
    - **strict** (optional): If False, ignores minor name mismatches
        such as underscore or character casing, otherwise must be exact
        match (defaults to False). 
    """
    if not strict:
        datumname = datumname.lower().replace(" ","_")
    for itemname,item in globals().items():
        if itemname.startswith("_") or itemname == 'Datum':
            continue
        try:
            if hasattr(item.name, crstype):
                itemname = getattr(item.name, crstype)
                if not strict:
                    itemname = itemname.lower().replace(" ","_")
                if datumname == itemname:
                    return item
        except:
            pass
    else:
        return None


##+datum     Datum name (see `proj -ld`)
class Datum:
    proj4 = "+datum"
    ogc_wkt = "DATUM"
    esri_wkt = "DATUM"

    name = None
    ellips = None
    datumshift = None
    
    def __init__(self, **kwargs):
        """
        A Datum defines the shape of the earth. 

        Arguments:

        - **name**: A pycrs.datums.DatumName instance with the name given by each supported format. 
        - **ellipsoid**: A pycrs.elements.ellipsoids.Ellipsoid instance.
        - **datumshift** (optional): A pycrs.elements.parameters.DatumShift instance. 
        """
        self.name = kwargs.get('name', self.name)
        self.ellips = kwargs.get('ellipsoid', self.ellips)
        self.datumshift = kwargs.get('datumshift', self.datumshift)

    def to_proj4(self):
        if self.datumshift:
            return "%s %s" % (self.ellips.to_proj4(), self.datumshift.to_proj4())
        elif isinstance(self, Unknown):
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

class DatumName:
    def __init__(self, proj4="", ogc_wkt="", esri_wkt=""):
        self.proj4 = proj4
        self.ogc_wkt = ogc_wkt
        self.esri_wkt = esri_wkt
        

# Specific predefined datum classes
class WGS84(Datum):
    name = DatumName(
                proj4 = "WGS84",
                ogc_wkt = "WGS_1984",
                esri_wkt = "D_WGS_1984",
                )

    ellips = ellipsoids.WGS84()
    datumshift = None

class WGS72_BE(Datum):
    name = DatumName(
                proj4 = "", # no datum name, just ellips + towgs84 params...
                ogc_wkt = "WGS_1972_Transit_Broadcast_Ephemeris",
                esri_wkt = "D_WGS_1972_BE",
                )

    ellips = ellipsoids.WGS72()
    datumshift = parameters.DatumShift([0,0,1.9,0,0,0.814,-0.38])

class NAD83(Datum):
    name = DatumName(
                proj4 = "NAD83", # no datum name, just ellips + towgs84 params...
                ogc_wkt = "North_American_Datum_1983",
                esri_wkt = "D_North_American_1983",
                )

    ellips = ellipsoids.GRS80()
    datumshift = None

class NAD27(Datum):
    name = DatumName(
                proj4 = "NAD27",
                ogc_wkt = "D_North_American_1927",
                esri_wkt = "D_North_American_1927",
                )
    
    ellips = ellipsoids.Clarke1866()
    datumshift = None

class SphereArcInfo(Datum):
    name = DatumName(
                proj4 = "", # no name
                ogc_wkt = "D_Sphere_ARC_INFO", # confirmed but odd that uses D_
                esri_wkt = "D_Sphere_ARC_INFO",
                )

    ellips = ellipsoids.SphereArcInfo()
    datumshift = None

class Unknown(Datum):
    name = DatumName(
                proj4 = "", # no datum name, just ellips + towgs84 params...
                ogc_wkt = "Unknown",
                esri_wkt = "Unknown",
                )

    ellips = ellipsoids.Unknown()
    datumshift = None
