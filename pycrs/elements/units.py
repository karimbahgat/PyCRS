

def find(unitname, crstype, strict=False):
    if not strict:
        unitname = unitname.lower()
    for itemname,item in globals().items():
        if itemname.startswith("_"):
            continue
        try:
            if hasattr(item, crstype):
                itemname = getattr(item, crstype)
                # compare
                if not strict:
                    itemname = itemname.lower()
                if unitname == itemname:
                    return item
                # special handling of wkt meters which has multiple possibilities
                elif isinstance(item(), Meter) and crstype.endswith("wkt") and not strict and unitname in ("meters","meter","metre","m"):
                    return item
        except:
            pass
    else:
        return None




class Meter:
    to_meter = 1.0
    proj4 = "m"
    ogc_wkt = "Meters" # or is it metre?? sometimes even Meter?
    esri_wkt = "Meter"

class Degree:
    # "For angular units, the conversion factor is the scalar value that converts the described units into radians."
    to_radians = 0.017453292519943295
    proj4 = "degrees"
    ogc_wkt = "degree"
    esri_wkt = "Degree"

class US_Feet:
    to_meter = 0.304800609601219241
    proj4 = "us-ft"
    ogc_wkt = "Foot_US"
    esri_wkt = "Foot_US"

class International_Feet:
    to_meter = 0.3048
    proj4 = "ft"
    ogc_wkt = "Foot"
    esri_wkt = "Foot"

class Unknown:
    to_meter = None
    proj4 = ""
    ogc_wkt = "Unknown"
    esri_wkt = "Unknown"
