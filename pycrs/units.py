

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
                elif isinstance(itemname, Meter) and crstype.endswith("wkt") and not strict and unitname in ("meters","meter","metre"):
                    return item
        except:
            pass
    else:
        return None




class Meter:
    proj4 = "m"
    ogc_wkt = "Meters" # or is it metre?? sometimes even Meter?
    esri_wkt = "Meter"

class Degree:
    proj4 = "degrees"
    ogc_wkt = "degree"
    esri_wkt = "Degree"

class Feet:
    proj4 = "..."
    ogc_wkt = "Foot_US"
    esri_wkt = "Foot_US"
