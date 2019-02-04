"""
Named projection classes that can be created or parsed. 
"""

def find(projname, crstype, strict=False):
    """
    Search for a projection name located in this module.

    Arguments:

    - **projname**: The projection name to search for.
    - **crstype**: Which CRS naming convention to search (different
        CRS formats have different names for the same projection).
    - **strict** (optional): If False, ignores minor name mismatches
        such as underscore or character casing, otherwise must be exact
        match (defaults to False). 
    """
    if not strict:
        projname = projname.lower().replace(" ","_")
    for itemname,item in globals().items():
        if itemname.startswith("_"):
            continue
        try:
            if hasattr(item.name, crstype):
                itemname = getattr(item.name, crstype)
                if not strict:
                    itemname = itemname.lower().replace(" ","_")
                if projname == itemname:
                    return item
        except:
            pass
    else:
        return None



##+proj      Projection name (see `proj -l`)
class Projection:
    proj4 = "+proj"
    ogc_wkt = "PROJECTION"
    esri_wkt = "PROJECTION"

    name = None
    
    def __init__(self, **kwargs):
        """
        A generic container for the specific projection used.

        Args:

        - **name**: A pycrs.projections.ProjName instance with the name given by each supported format. 
        """
        self.name = kwargs.get('name', self.name)

    def to_proj4(self):
        return "+proj=%s" %self.name.proj4

    def to_ogc_wkt(self):
        return 'PROJECTION["%s"]' %self.name.ogc_wkt

    def to_esri_wkt(self):
        return 'PROJECTION["%s"]' %self.name.esri_wkt

class ProjName:
    def __init__(self, proj4="", ogc_wkt="", esri_wkt=""):
        self.proj4 = proj4
        self.ogc_wkt = ogc_wkt
        self.esri_wkt = esri_wkt




# Specific predefined ellipsoid classes    
class Robinson(Projection):
    name = ProjName(
        proj4 = "robin",
        ogc_wkt = "Robinson",
        esri_wkt = "Robinson",
        )

class UTM(Projection):
    name = ProjName(
        proj4 = "utm",
        ogc_wkt = "Transverse_Mercator",
        esri_wkt = "Transverse_Mercator",
        )

class ObliqueMercator(Projection):
    name = ProjName(
        proj4 = "omerc",
        ogc_wkt = "Hotine_Oblique_Mercator_Two_Point_Natural_Origin", #"Hotine_Oblique_Mercator"
        esri_wkt = "Hotine_Oblique_Mercator_Two_Point_Natural_Origin", #"Hotine_Oblique_Mercator_Azimuth_Natural_Origin"
        )
    
class AlbersEqualArea(Projection):
    name = ProjName(
        proj4 = "aea",
        ogc_wkt = "Albers_Conic_Equal_Area",
        esri_wkt = "Albers",
        )

class CylindricalEqualArea(Projection):
    name = ProjName(
        proj4 = "cea",
        ogc_wkt = "Cylindrical_Equal_Area",
        esri_wkt = "Cylindrical_Equal_Area",
        )
    
class EquiDistantConic(Projection):
    name = ProjName(
        proj4 = "eqdc",
        ogc_wkt = "Equidistant_Conic",
        esri_wkt = "Equidistant_Conic",
        )

class EquiDistantCylindrical(Projection):
    # same as equirectangular...?
    name = ProjName(
        proj4 = "eqc",
        ogc_wkt = "Equidistant_Cylindrical",
        esri_wkt = "Equidistant_Cylindrical",
        )

class EquiRectangular(Projection):
    # same as equidistant cylindrical
    name = ProjName(
        proj4 = "eqc",
        ogc_wkt = "Equirectangular",
        esri_wkt = "Equirectangular",
        )

class TransverseMercator(Projection):
    name = ProjName(
        proj4 = "tmerc",
        ogc_wkt = "Transverse_Mercator",
        esri_wkt = "Transverse_Mercator",
        )

class GallStereographic(Projection):
    name = ProjName(
        proj4 = "gall",
        ogc_wkt = "Gall_Stereographic",
        esri_wkt = "Gall_Stereographic",
        )

class Gnomonic(Projection):
    name = ProjName(
        proj4 = "gnom",
        ogc_wkt = "Gnomonic",
        esri_wkt = "Gnomonic",
        )

class LambertAzimuthalEqualArea(Projection):
    name = ProjName(
        proj4 = "laea",
        ogc_wkt = "Lambert_Azimuthal_Equal_Area",
        esri_wkt = "Lambert_Azimuthal_Equal_Area",
        )

class MillerCylindrical(Projection):
    name = ProjName(
        proj4 = "mill",
        ogc_wkt = "Miller_Cylindrical",
        esri_wkt = "Miller_Cylindrical",
        )

class Mollweide(Projection):
    name = ProjName(
        proj4 = "moll",
        ogc_wkt = "Mollweide",
        esri_wkt = "Mollweide",
        )

class ObliqueStereographic(Projection):
    name = ProjName(
        proj4 = "sterea",
        ogc_wkt = "Oblique_Stereographic",
        esri_wkt = "Oblique Stereographic", #"Stereographic_North_Pole"
        )

class Orthographic(Projection):
    name = ProjName(
        proj4 = "ortho",
        ogc_wkt = "Orthographic",
        esri_wkt = "Orthographic",
        )

class Stereographic(Projection):
    name = ProjName(
        proj4 = "stere",
        ogc_wkt = "Stereographic",
        esri_wkt = "Stereographic",
        )

class PolarStereographic(Projection):
    name = ProjName(
        proj4 = "stere",
        ogc_wkt = "Polar_Stereographic", # could also be just stereographic
        esri_wkt = "Stereographic", # but also spelled with additional _South/North_Pole, for the same projection and diff params (maybe just for humans)?...
        )

class Sinusoidal(Projection):
    name = ProjName(
        proj4 = "sinu",
        ogc_wkt = "Sinusoidal",
        esri_wkt = "Sinusoidal",
        )

class VanDerGrinten(Projection):
    name = ProjName(
        proj4 = "vandg",
        ogc_wkt = "VanDerGrinten",
        esri_wkt = "Van_der_Grinten_I",
        )

class LambertConformalConic(Projection):
    name = ProjName(
        proj4 = "lcc",
        ogc_wkt = "Lambert_Conformal_Conic", # possible has some variants
        esri_wkt = "Lambert_Conformal_Conic",
        )

class Krovak(Projection):
    name = ProjName(
        proj4 = "krovak",
        ogc_wkt = "Krovak",
        esri_wkt = "Krovak",
        )

class NearSidedPerspective(Projection):
    name = ProjName(
        proj4 = "nsper",
        ogc_wkt = "Near_sided_perspective",
        esri_wkt = "Near_sided_perspective", # not confirmed
        )

class TiltedPerspective(Projection):
    name = ProjName(
        proj4 = "tsper",
        ogc_wkt = "Tilted_perspective",
        esri_wkt = "Tilted_perspective", # not confirmed
        )

class InteruptedGoodeHomolosine(Projection):
    name = ProjName(
        proj4 = "igh",
        ogc_wkt = "Interrupted_Goodes_Homolosine",
        esri_wkt = "Interrupted_Goodes_Homolosine",
        )

class Larrivee(Projection):
    name = ProjName(
        proj4 = "larr",
        ogc_wkt = "Larrivee",
        esri_wkt = "Larrivee", # not confirmed
        )

class LamberEqualAreaConic(Projection):
    name = ProjName(
        proj4 = "leac",
        ogc_wkt = "Lambert_Equal_Area_Conic",
        esri_wkt = "Lambert_Equal_Area_Conic", # not confirmed
        )

class Mercator(Projection):
    name = ProjName(
        proj4 = "merc",
        ogc_wkt = "Mercator", # has multiple varieties
        esri_wkt = "Mercator",
        )

class ObliqueCylindricalEqualArea(Projection):
    name = ProjName(
        proj4 = "ocea",
        ogc_wkt = "Oblique_Cylindrical_Equal_Area",
        esri_wkt = "Oblique_Cylindrical_Equal_Area",
        )

class Polyconic(Projection):
    name = ProjName(
        proj4 = "poly",
        ogc_wkt = "Polyconic",
        esri_wkt = "Polyconic",
        )

class EckertIV(Projection):
    name = ProjName(
        proj4 = "eck4",
        ogc_wkt = "Eckert_IV",
        esri_wkt = "Eckert_IV",
        )

class EckertVI(Projection):
    name = ProjName(
        proj4 = "eck6",
        ogc_wkt = "Eckert_VI",
        esri_wkt = "Eckert_VI",
        )

class AzimuthalEquidistant(Projection):
    name = ProjName(
        proj4 = "aeqd",
        ogc_wkt = "Azimuthal_Equidistant",
        esri_wkt = "Azimuthal_Equidistant",
        )

class GeostationarySatellite(Projection):
    name = ProjName(
        proj4 = "geos",
        ogc_wkt = "Geostationary_Satellite",
        esri_wkt = "Geostationary_Satellite",
        )







    

    


