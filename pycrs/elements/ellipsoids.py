

def find(ellipsname, crstype, strict=False):
    if not strict:
        ellipsname = ellipsname.lower().replace(" ","_")
    for itemname,item in globals().items():
        if itemname.startswith("_") or itemname == 'Ellipsoid':
            continue
        try:
            if hasattr(item.name, crstype):
                itemname = getattr(item.name, crstype)
                if not strict:
                    itemname = itemname.lower().replace(" ","_")
                if ellipsname == itemname:
                    return item
        except:
            pass
    else:
        return None


##+ellps     Ellipsoid name (see `proj -le`)
class Ellipsoid:
    proj4 = "+ellps"
    ogc_wkt = "SPHEROID"
    esri_wkt = "SPHEROID"

    name = None
    semimaj_ax = None
    inv_flat = None

    def __init__(self, **kwargs):
        """
        The ellipsoid that defines the shape of the earth. 

        Arguments:

        - **name**: A pycrs.ellipsoids.EllipsoidName instance with the name given by each supported format. 
        - **semimaj_ax**: A float representing the coordinate position of the semimajor axis.
        - **inv_flat**: A float representing the inverse flattening factor. 
        """
        self.name = kwargs.get('name', self.name)
        self.semimaj_ax = kwargs.get('semimaj_ax', self.semimaj_ax)
        self.inv_flat = kwargs.get('inv_flat', self.inv_flat)

    def to_proj4(self):
        if isinstance(self, Unknown):
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

class EllipsoidName:
    def __init__(self, proj4="", ogc_wkt="", esri_wkt=""):
        self.proj4 = proj4
        self.ogc_wkt = ogc_wkt
        self.esri_wkt = esri_wkt


# Specific predefined ellipsoid classes
class WGS84(Ellipsoid):
    name = EllipsoidName(
                proj4 = "WGS84",
                ogc_wkt = "WGS_1984",
                esri_wkt = "WGS_1984",
                )
    
    semimaj_ax = 6378137
    inv_flat = 298.257223563

class WGS72(Ellipsoid):
    name = EllipsoidName(
                proj4 = "WGS72",
                ogc_wkt = "WGS 72",
                esri_wkt = "WGS_1972",
                )

    semimaj_ax = 6378135
    inv_flat = 298.26

class International(Ellipsoid):
    name = EllipsoidName(
                proj4 = "intl",
                ogc_wkt = "International_1924",
                esri_wkt = "International_1924",
                )

    semimaj_ax = 6378388.0
    inv_flat = 297.0

class GRS80(Ellipsoid):
    name = EllipsoidName(
                proj4 = "GRS80",
                ogc_wkt = "GRS_1980",
                esri_wkt = "GRS_1980",
                )

    semimaj_ax = 6378137.0
    inv_flat = 298.257222101

class Clarke1866(Ellipsoid):
    name = EllipsoidName(
                proj4 = "clrk66",
                ogc_wkt = "Clarke_1866",
                esri_wkt = "Clarke_1866",
                )

    semimaj_ax = 6378206.4
    inv_flat = 294.9786982

class Airy1830(Ellipsoid):
    name = EllipsoidName(
                proj4 = "airy",
                ogc_wkt = "Airy 1830",
                esri_wkt = "Airy_1830",
                )

    semimaj_ax = 6377563.396
    inv_flat = 299.3249646

class SphereArcInfo(Ellipsoid):
    name = EllipsoidName(
                proj4 = "", # no name
                ogc_wkt = "Sphere_ARC_INFO",
                esri_wkt = "Sphere_ARC_INFO",
                )

    semimaj_ax = 6370997.0
    inv_flat = 0.0

class Krassowsky1940(Ellipsoid):
    name = EllipsoidName(
                proj4 = "krass",
                ogc_wkt = "Krassowsky 1940",
                esri_wkt = "Krassowsky_1940",
                )

    semimaj_ax = 6378245.0
    inv_flat = 298.3

class Bessel1841(Ellipsoid):
    name = EllipsoidName(
                proj4 = "bessel",
                ogc_wkt = "Bessel 1841",
                esri_wkt = "Bessel_1841",
                )

    semimaj_ax = 6377397.155
    inv_flat = 299.1528128

class Unknown(Ellipsoid):
    name = EllipsoidName(
                proj4 = "",
                ogc_wkt = "Unknown",
                esri_wkt = "Unknown",
                )

    # values have to be set manually in Ellipsoid class
    semimaj_ax = None
    inv_flat = None







    
