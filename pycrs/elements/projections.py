

def find(projname, crstype, strict=False):
    if not strict:
        projname = projname.lower().replace(" ","_")
    for itemname,item in globals().items():
        if itemname.startswith("_"):
            continue
        try:
            if hasattr(item, crstype):
                itemname = getattr(item, crstype)
                if not strict:
                    itemname = itemname.lower().replace(" ","_")
                if projname == itemname:
                    return item
        except:
            pass
    else:
        return None



    

class Robinson:
    proj4 = "robin"
    ogc_wkt = "Robinson"
    esri_wkt = "Robinson"

class UTM:
    proj4 = "utm"
    ogc_wkt = "Transverse_Mercator"
    esri_wkt = "Transverse_Mercator"

class ObliqueMercator:
    proj4 = "omerc"
    ogc_wkt = "Hotine_Oblique_Mercator_Two_Point_Natural_Origin" #"Hotine_Oblique_Mercator"
    esri_wkt = "Hotine_Oblique_Mercator_Two_Point_Natural_Origin" #"Hotine_Oblique_Mercator_Azimuth_Natural_Origin"
    
class AlbersEqualArea:
    proj4 = "aea"
    ogc_wkt = "Albers_Conic_Equal_Area"
    esri_wkt = "Albers"

class CylindricalEqualArea:
    proj4 = "cea"
    ogc_wkt = "Cylindrical_Equal_Area"
    esri_wkt = "Cylindrical_Equal_Area"
    
class EquiDistantConic:
    proj4 = "eqdc"
    ogc_wkt = "Equidistant_Conic" 
    esri_wkt = "Equidistant_Conic" 

class EquiDistantCylindrical:
    # same as equirectangular...?
    proj4 = "eqc"
    ogc_wkt = "Equidistant_Cylindrical"
    esri_wkt = "Equidistant_Cylindrical"

class EquiRectangular:
    # same as equidistant cylindrical
    proj4 = "eqc"
    ogc_wkt = "Equirectangular"
    esri_wkt = "Equirectangular"

class TransverseMercator:
    proj4 = "tmerc"
    ogc_wkt = "Transverse_Mercator"
    esri_wkt = "Transverse_Mercator"

class GallStereographic:
    proj4 = "gall"
    ogc_wkt = "Gall_Stereographic"
    esri_wkt = "Gall_Stereographic"

class Gnomonic:
    proj4 = "gnom"
    ogc_wkt = "Gnomonic"
    esri_wkt = "Gnomonic"

class LambertAzimuthalEqualArea:
    proj4 = "laea"
    ogc_wkt = "Lambert_Azimuthal_Equal_Area"
    esri_wkt = "Lambert_Azimuthal_Equal_Area"

class MillerCylindrical:
    proj4 = "mill"
    ogc_wkt = "Miller_Cylindrical"
    esri_wkt = "Miller_Cylindrical"

class Mollweide:
    proj4 = "moll"
    ogc_wkt = "Mollweide"
    esri_wkt = "Mollweide"

class ObliqueStereographic:
    proj4 = "sterea"
    ogc_wkt = "Oblique_Stereographic"
    esri_wkt = "Oblique Stereographic" #"Stereographic_North_Pole"

class Orthographic:
    proj4 = "ortho"
    ogc_wkt = "Orthographic"
    esri_wkt = "Orthographic"

class Stereographic:
    proj4 = "stere"
    ogc_wkt = "Stereographic" 
    esri_wkt = "Stereographic" 

class PolarStereographic:
    proj4 = "stere"
    ogc_wkt = "Polar_Stereographic" # could also be just stereographic
    esri_wkt = "Stereographic" # but also spelled with additional _South/North_Pole, for the same projection and diff params (maybe just for humans)?...

class Sinusoidal:
    proj4 = "sinu"
    ogc_wkt = "Sinusoidal"
    esri_wkt = "Sinusoidal"

class VanDerGrinten:
    proj4 = "vandg"
    ogc_wkt = "VanDerGrinten"
    esri_wkt = "Van_der_Grinten_I"

class LambertConformalConic:
    proj4 = "lcc"
    ogc_wkt = "Lambert_Conformal_Conic" # possible has some variants
    esri_wkt = "Lambert_Conformal_Conic"

class Krovak:
    proj4 = "krovak"
    ogc_wkt = "Krovak"
    esri_wkt = "Krovak"

class NearSidedPerspective:
    proj4 = "nsper"
    ogc_wkt = "Near_sided_perspective"
    esri_wkt = "Near_sided_perspective" # not confirmed

class TiltedPerspective:
    proj4 = "tsper"
    ogc_wkt = "Tilted_perspective"
    esri_wkt = "Tilted_perspective" # not confirmed

class InteruptedGoodeHomolosine:
    proj4 = "igh"
    ogc_wkt = "Interrupted_Goodes_Homolosine"
    esri_wkt = "Interrupted_Goodes_Homolosine"

class Larrivee:
    proj4 = "larr"
    ogc_wkt = "Larrivee"
    esri_wkt = "Larrivee" # not confirmed

class LamberEqualAreaConic:
    proj4 = "leac"
    ogc_wkt = "Lambert_Equal_Area_Conic"
    esri_wkt = "Lambert_Equal_Area_Conic" # not confirmed

class Mercator:
    proj4 = "merc"
    ogc_wkt = "Mercator" # has multiple varieties
    esri_wkt = "Mercator"

class ObliqueCylindricalEqualArea:
    proj4 = "ocea"
    ogc_wkt = "Oblique_Cylindrical_Equal_Area"
    esri_wkt = "Oblique_Cylindrical_Equal_Area"

class Polyconic:
    proj4 = "poly"
    ogc_wkt = "Polyconic"
    esri_wkt = "Polyconic"

class EckertIV:
    proj4 = "eck4"
    ogc_wkt = "Eckert_IV"
    esri_wkt = "Eckert_IV"

class EckertVI:
    proj4 = "eck6"
    ogc_wkt = "Eckert_VI"
    esri_wkt = "Eckert_VI"

class AzimuthalEquidistant:
    proj4 = "aeqd"
    ogc_wkt = "Azimuthal_Equidistant"
    esri_wkt = "Azimuthal_Equidistant"

class GeostationarySatellite:
    proj4 = "geos"
    ogc_wkt = "Geostationary_Satellite"
    esri_wkt = "Geostationary_Satellite"







    

    


