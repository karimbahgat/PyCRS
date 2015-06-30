

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
