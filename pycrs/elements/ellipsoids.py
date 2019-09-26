"""
Named ellipsoid classes that can be created or parsed. 
"""

from . import parameters


def find(ellipsname, crstype, strict=False):
    """
    Search for a ellipsoid name located in this module.

    Arguments:

    - **ellipsname**: The ellipsoid name to search for.
    - **crstype**: Which CRS naming convention to search (different
        CRS formats have different names for the same ellipsoid).
    - **strict** (optional): If False, ignores minor name mismatches
        such as underscore or character casing, otherwise must be exact
        match (defaults to False). 
    """
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
    semimin_ax = None
    flat = None
    inv_flat = None

    def __init__(self, **kwargs):
        """
        The ellipsoid that defines the shape of the earth.
        To sufficiently define an ellipsoid, either set semimaj_ax + semimin_ax, semimaj_ax + flat,
        or semimaj_ax + inv_flat. 

        Arguments:

        - **name**: A pycrs.ellipsoids.EllipsoidName instance with the name given by each supported format. 
        - **semimaj_ax**: A pycrs.parameters.SemiMajorRadius representing the radius of the semimajor axis.
        - **semimin_ax**: A pycrs.parameters.SemiMinorRadius representing the radius of the semiminor axis.
        - **flat**: A pycrs.parameters.Flattening representing the flattening factor. 
        - **inv_flat**: A pycrs.parameters.InverseFlattening representing the inverse flattening factor. 
        """
        self.name = kwargs.get('name', self.name)
        self.semimaj_ax = kwargs.get('semimaj_ax', self.semimaj_ax)
        self.semimin_ax = kwargs.get('semimin_ax', self.semimin_ax)
        self.flat = kwargs.get('flat', self.flat)
        self.inv_flat = kwargs.get('inv_flat', self.inv_flat)

    def _get_flat(self):
        if self.flat:
            # flattening given directly
            flat = self.flat.value
        elif self.semimaj_ax and self.semimin_ax:
            # calculate flattening from semimajor and minor radius
            a = float(self.semimaj_ax.value)
            b = float(self.semimin_ax.value)
            flat = (a - b) / float(a)
        elif self.inv_flat:
            # calculate flattening from the inverse flattening
            flat = 1 / float(self.inv_flat.value)
        else:
            raise Exception("Cannot get ellipsoid flattening, needs either semimaj_ax + semimin_ax, semimaj_ax + flat, or semimaj_ax + inv_flat")
        return flat

    def _get_wkt_invflat(self):
        # WKT is special in that it falsely sets the inverse flattening to 0 for perfect spheres
        # mathematically, when flattening is 0, then the inverse undefined
        if self.inv_flat:
            inv_flat = self.inv_flat.value
        else:
            flat = self._get_flat()
            if flat == 0:
                inv_flat = 0 # special WKT handling
            else:
                inv_flat = 1 / float(flat)
        return inv_flat

    def to_proj4(self):
        proj4 = []
        if self.name.proj4:
            # ellipsoid name
            proj4.append("+ellps=%s" % self.name.proj4)
        if self.semimaj_ax:
            proj4.append(self.semimaj_ax.to_proj4())
            # include just one of semiminor, flattening, or inverse flattening (all aspects of the same)
            # TODO: If has name matching a predefined ellipsoid, maybe consider comparing and only reporting
            # those values that differ. 
            if self.semimin_ax:
                proj4.append(self.semimin_ax.to_proj4())
            elif self.inv_flat:
                proj4.append(self.inv_flat.to_proj4())
            elif self.flat:
                proj4.append(self.flat.to_proj4())
        if not proj4:
            raise Exception("Not enough information to export the ellipsoid to proj4")
        return " ".join(proj4)

    def to_ogc_wkt(self):
        inv_flat = self._get_wkt_invflat()
        return 'SPHEROID["%s", %s, %s]' % (self.name.ogc_wkt, self.semimaj_ax.value, inv_flat)
    
    def to_esri_wkt(self):
        inv_flat = self._get_wkt_invflat()
        return 'SPHEROID["%s", %s, %s]' % (self.name.esri_wkt, self.semimaj_ax.value, inv_flat)

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
    
    semimaj_ax = parameters.SemiMajorRadius(6378137.0)
    inv_flat = parameters.InverseFlattening(298.257223563)

class WGS72(Ellipsoid):
    name = EllipsoidName(
                proj4 = "WGS72",
                ogc_wkt = "WGS 72",
                esri_wkt = "WGS_1972",
                )

    semimaj_ax = parameters.SemiMajorRadius(6378135.0)
    inv_flat = parameters.InverseFlattening(298.26)

class International(Ellipsoid):
    name = EllipsoidName(
                proj4 = "intl",
                ogc_wkt = "International_1924",
                esri_wkt = "International_1924",
                )

    semimaj_ax = parameters.SemiMajorRadius(6378388.0)
    inv_flat = parameters.InverseFlattening(297.0)

class GRS80(Ellipsoid):
    name = EllipsoidName(
                proj4 = "GRS80",
                ogc_wkt = "GRS_1980",
                esri_wkt = "GRS_1980",
                )

    semimaj_ax = parameters.SemiMajorRadius(6378137.0)
    inv_flat = parameters.InverseFlattening(298.257222101)

class Clarke1866(Ellipsoid):
    name = EllipsoidName(
                proj4 = "clrk66",
                ogc_wkt = "Clarke_1866",
                esri_wkt = "Clarke_1866",
                )

    semimaj_ax = parameters.SemiMajorRadius(6378206.4)
    inv_flat = parameters.InverseFlattening(294.9786982)

class Clarke1880(Ellipsoid):
    name = EllipsoidName(
                proj4 = "clrk80",
                ogc_wkt = "Clarke 1880 (RGS)",
                esri_wkt = "Clarke_1880_RGS",
                )

    semimaj_ax = parameters.SemiMajorRadius(6378249.145)
    inv_flat = parameters.InverseFlattening(293.465)

class Airy1830(Ellipsoid):
    name = EllipsoidName(
                proj4 = "airy",
                ogc_wkt = "Airy 1830",
                esri_wkt = "Airy_1830",
                )

    semimaj_ax = parameters.SemiMajorRadius(6377563.396)
    inv_flat = parameters.InverseFlattening(299.3249646)

class SphereArcInfo(Ellipsoid):
    name = EllipsoidName(
                proj4 = "", # no name
                ogc_wkt = "Sphere_ARC_INFO",
                esri_wkt = "Sphere_ARC_INFO",
                )

    semimaj_ax = parameters.SemiMajorRadius(6370997.0)
    flat = parameters.Flattening(0.0)

class Krassowsky1940(Ellipsoid):
    name = EllipsoidName(
                proj4 = "krass",
                ogc_wkt = "Krassowsky 1940",
                esri_wkt = "Krassowsky_1940",
                )

    semimaj_ax = parameters.SemiMajorRadius(6378245.0)
    inv_flat = parameters.InverseFlattening(298.3)

class Bessel1841(Ellipsoid):
    name = EllipsoidName(
                proj4 = "bessel",
                ogc_wkt = "Bessel 1841",
                esri_wkt = "Bessel_1841",
                )

    semimaj_ax = parameters.SemiMajorRadius(6377397.155)
    inv_flat = parameters.InverseFlattening(299.1528128)

class Unknown(Ellipsoid):
    name = EllipsoidName(
                proj4 = "",
                ogc_wkt = "Unknown",
                esri_wkt = "Unknown",
                )

    # values have to be set manually in Ellipsoid class
    semimaj_ax = None
    inv_flat = None







    
