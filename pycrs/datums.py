
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


class Unknown:
    proj4 = "unknown" # no datum name, just ellips + towgs84 params...
    ogc_wkt = "Unknown"
    esri_wkt = "Unknown"

    ellipsdef = "" # ellipsoids.WGS72()
    to_wgs84 = None,None
