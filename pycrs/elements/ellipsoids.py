

def find(ellipsname, crstype, strict=False):
    if not strict:
        ellipsname = ellipsname.lower().replace(" ","_")
    for itemname,item in globals().items():
        if itemname.startswith("_"):
            continue
        try:
            if hasattr(item, crstype):
                itemname = getattr(item, crstype)
                if not strict:
                    itemname = itemname.lower().replace(" ","_")
                if ellipsname == itemname:
                    return item
        except:
            pass
    else:
        return None





class WGS84:
    proj4 = "WGS84"
    ogc_wkt = "WGS_1984"
    esri_wkt = "WGS_1984"
    
    semimaj_ax = 6378137
    inv_flat = 298.257223563
    

class WGS72:
    proj4 = "WGS72"
    ogc_wkt = "WGS 72"
    esri_wkt = "WGS_1972"

    semimaj_ax = 6378135
    inv_flat = 298.26

class International:
    proj4 = "intl"
    ogc_wkt = "International_1924"
    esri_wkt = "International_1924"

    semimaj_ax = 6378388.0
    inv_flat = 297.0

class GRS80:
    proj4 = "GRS80"
    ogc_wkt = "GRS_1980"
    esri_wkt = "GRS_1980"

    semimaj_ax = 6378137.0
    inv_flat = 298.257222101

class Clarke1866:
    proj4 = "clrk66"
    ogc_wkt = "Clarke_1866"
    esri_wkt = "Clarke_1866"

    semimaj_ax = 6378206.4
    inv_flat = 294.9786982

class Airy1830:
    proj4 = "airy"
    ogc_wkt = "Airy 1830"
    esri_wkt = "Airy_1830"

    semimaj_ax = 6377563.396
    inv_flat = 299.3249646

class SphereArcInfo:
    proj4 = "" # no name
    ogc_wkt = "Sphere_ARC_INFO"
    esri_wkt = "Sphere_ARC_INFO"

    semimaj_ax = 6370997.0
    inv_flat = 0.0

class Krassowsky1940:
    proj4 = "krass"
    ogc_wkt = "Krassowsky 1940"
    esri_wkt = "Krassowsky_1940"

    semimaj_ax = 6378245.0
    inv_flat = 298.3

class Bessel1841:
    proj4 = "bessel"
    ogc_wkt = "Bessel 1841"
    esri_wkt = "Bessel_1841"

    semimaj_ax = 6377397.155
    inv_flat = 299.1528128

class Unknown:
    proj4 = ""
    ogc_wkt = "Unknown"
    esri_wkt = "Unknown"

    # values have to be set manually in Ellipsoid class
    semimaj_ax = None
    inv_flat = None







    
