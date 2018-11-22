

def find(unitname, crstype, strict=False):
    if not strict:
        unitname = unitname.lower()
    for itemname,item in globals().items():
        if itemname.startswith("_"):
            continue
        try:
            if hasattr(item.unitname, crstype):
                itemname = getattr(item.unitname, crstype)
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


##################
# Unit base class
# +unit and +to_meter are what makes up 'UNIT["Meter",1.0]'
class Unit:
    ogc_wkt = "UNIT"
    esri_wkt = "UNIT"

    unitname = None
    unitmultiplier = None
    
    def __init__(self, **kwargs):
        """
        Distance unit parameter. 

        Args:

        - **unitname**: A pycrs.elements.units.UnitName instance with the name given by each supported format. 
        - **unitmultiplier**: A pycrs.elements.units.UnitMultiplier instance. 
        """
        self.unitname = kwargs.get('unitname', self.unitname)
        self.unitmultiplier = kwargs.get('unitmultiplier', self.unitmultiplier)

    def to_proj4(self):
        # always use unit type, or if unknown unit type use meter multiplier
        if isinstance(self, Unknown):
            return "+to_meter=%r" % self.unitmultiplier.value
        else:
            return "+units=%s" % self.unitname.proj4

    def to_ogc_wkt(self):
        return 'UNIT["%s", %r]' %(self.unitname.ogc_wkt, self.unitmultiplier.value)

    def to_esri_wkt(self):
        return 'UNIT["%s", %r]' %(self.unitname.esri_wkt, self.unitmultiplier.value)

##+units     meters, US survey feet, etc.
class UnitName:
    def __init__(self, proj4="", ogc_wkt="", esri_wkt=""):
        self.proj4 = proj4
        self.ogc_wkt = ogc_wkt
        self.esri_wkt = esri_wkt

##+to_meter  Multiplier to convert map units to 1.0m
class UnitMultiplier: 
    def __init__(self, value):
        """
        The multiplier factor for converting coordinate units to the coordinate system reference unit.
        For linear units this is usually to meters, for angular units usually radians. 

        Arguments:

        - **value**: the meter multiplier, as a float.
        """
        self.value = value


###################################
# Specific predefined unit classes

class Meter(Unit):
    unitname = UnitName(
                        proj4 = "m",
                        ogc_wkt = "Meters", # or is it metre?? sometimes even Meter?
                        esri_wkt = "Meter",
                        )
    unitmultiplier = UnitMultiplier(1.0)

class Degree(Unit):
    unitname = UnitName(
                        proj4 = "degrees",
                        ogc_wkt = "degree",
                        esri_wkt = "Degree",
                        )
    unitmultiplier = UnitMultiplier(0.017453292519943295) # NOTE: "For angular units, the conversion factor is the scalar value that converts the described units into radians."

class US_Feet(Unit):
    unitname = UnitName(
                        proj4 = "us-ft",
                        ogc_wkt = "Foot_US",
                        esri_wkt = "Foot_US",
                        )
    unitmultiplier = UnitMultiplier(0.304800609601219241)

class International_Feet(Unit):
    unitname = UnitName(
                        proj4 = "ft",
                        ogc_wkt = "Foot",
                        esri_wkt = "Foot",
                        )
    unitmultiplier = UnitMultiplier(0.3048) 

class Unknown(Unit):
    unitname = UnitName(
                        proj4 = "",
                        ogc_wkt = "Unknown",
                        esri_wkt = "Unknown",
                        )
    unitmultiplier = UnitMultiplier(None)


