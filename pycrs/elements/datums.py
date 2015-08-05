

def find(datumname, crstype, strict=False):
    if not strict:
        datumname = datumname.lower().replace(" ","_")
    for itemname,item in globals().items():
        if itemname.startswith("_"):
            continue
        try:
            if hasattr(item, crstype):
                itemname = getattr(item, crstype)
                if not strict:
                    itemname = itemname.lower().replace(" ","_")
                if datumname == itemname:
                    return item
        except:
            pass
    else:
        return None

    


class WGS84:
    proj4 = "WGS84"
    ogc_wkt = "WGS_1984"
    esri_wkt = "D_WGS_1984"

    ellipsdef = "" # ellipsoids.WGS84()
    to_wgs84 = None

class WGS72_BE:
    proj4 = "" # no datum name, just ellips + towgs84 params...
    ogc_wkt = "WGS_1972_Transit_Broadcast_Ephemeris"
    esri_wkt = "D_WGS_1972_BE"

    ellipsdef = "" # ellipsoids.WGS72()
    to_wgs84 = 0,0,1.9,0,0,0.814,-0.38

class NAD83:
    proj4 = "NAD83" # no datum name, just ellips + towgs84 params...
    ogc_wkt = "North_American_Datum_1983"
    esri_wkt = "D_North_American_1983"

    ellipsdef = "" # ellipsoids.WGS72()
    to_wgs84 = None

class NAD27:
    proj4 = "NAD27"
    ogc_wkt = "D_North_American_1927"
    esri_wkt = "D_North_American_1927"
    
    ellipsdef = "" # ellipsoids...
    to_wgs84 = None

class SphereArcInfo:
    proj4 = "" # no name
    ogc_wkt = "D_Sphere_ARC_INFO" # confirmed but odd that uses D_
    esri_wkt = "D_Sphere_ARC_INFO"

    ellipsdef = "" # ellipsoids...
    to_wgs84 = None

class Unknown:
    proj4 = "" # no datum name, just ellips + towgs84 params...
    ogc_wkt = "Unknown"
    esri_wkt = "Unknown"

    ellipsdef = "" # ellipsoids.WGS72()
    to_wgs84 = None
