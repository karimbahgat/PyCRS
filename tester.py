import pycrs
import traceback



###########################
# Drawing routine for testing
def render_world(crs):
    import urllib2
    import json
    import pygeoj
    import pyagg
    import pyproj
    import random

    # load world borders
    raw = urllib2.urlopen("https://raw.githubusercontent.com/johan/world.geo.json/master/countries.geo.json").read()
    rawdict = json.loads(raw)
    data = pygeoj.load(data=rawdict)

    # convert coordinates
    fromproj = pyproj.Proj("+init=EPSG:4326")
    toproj = pyproj.Proj(crs.to_proj4())
    for feat in data:
        if feat.geometry.type == "Polygon":
            feat.geometry.coordinates = [zip(*pyproj.transform(fromproj, toproj, zip(*ring)[0], zip(*ring)[1]))
                                         for ring in feat.geometry.coordinates]
        elif feat.geometry.type == "MultiPolygon":
            feat.geometry.coordinates = [
                                        [zip(*pyproj.transform(fromproj, toproj, zip(*ring)[0], zip(*ring)[1]))
                                         for ring in poly]
                                         for poly in feat.geometry.coordinates]
    # get zoom area
    # NOTE: PYGEOJ data.bbox doesnt update.........FIX!
    data.add_all_bboxes()
    data.update_bbox()
    bbox = data.bbox

##    # to avoid inf bounds and no render in satellite view
##    xmins, ymins, xmaxs, ymaxs = zip(*(feat.geometry.bbox for feat in data))
##    inf = float("inf") 
##    xmaxs = (xmax for xmax in xmaxs if xmax != inf)
##    ymaxs = (ymax for ymax in ymaxs if ymax != inf)
##    bbox = (min(xmins), min(ymins), max(xmaxs), max(ymaxs)) 

    # set up drawing
    c = pyagg.Canvas(600,600)
    c.geographic_space()
    c.zoom_bbox(*bbox)
    c.zoom_out(1.3)

    # draw
    for feat in data:
        try: c.draw_geojson(feat.geometry,
                            fillcolor=tuple(random.randrange(255) for _ in range(3)),
                            outlinecolor="white")
        except:
            # NOTE: feat.__geo_interface__ is one level too high maybe??
            print("unable to draw?", feat.geometry)
    c.view()






# Source string generator
def sourcestrings(format):
    # TODO: now bunch of randoms, instead add only most commonly used ones
    yield pycrs.webscrape.crscode_to_string("esri", 54030, format)
    yield pycrs.webscrape.crscode_to_string("sr-org", 7898, format)
    yield pycrs.webscrape.crscode_to_string("sr-org", 6978, format)
    yield pycrs.webscrape.crscode_to_string("epsg", 4324, format)
    yield pycrs.webscrape.crscode_to_string("sr-org", 6618, format)
    yield pycrs.webscrape.crscode_to_string("sr-org", 22, format)
    yield pycrs.webscrape.crscode_to_string("esri", 54031, format)
    # add more...





# Testing format outputs
def testoutputs(crs):
    print("To:\n")
    try: result = crs.to_ogc_wkt()
    except: result = traceback.format_exc()
    print("ogc_wkt: %s \n" % result)

    try: result = crs.to_esri_wkt()
    except: result = traceback.format_exc()
    print("esri_wkt: %s \n" % result)
          
    try: result = crs.to_proj4()
    except: result = traceback.format_exc()
    print("proj4: %s \n" % result)




# Misc crs for testing
#crs = pycrs.webscrape.crscode_to_string("esri", 54030, "proj4")
#crs = pycrs.webscrape.crscode_to_string("sr-org", 6978, "proj4")
#crs = pycrs.parser.from_sr_code(7898)
#crs = pycrs.parser.from_epsg_code(4324)
#crs = pycrs.parser.from_sr_code(6618)
#crs = pycrs.parser.from_sr_code(22)
#crs = pycrs.parser.from_esri_code(54031)
#proj4 = "+proj=longlat +ellps=WGS84 +datum=WGS84"
#proj4 = "+proj=aea +lat_1=24 +lat_2=31.5 +lat_0=24 +lon_0=-84 +x_0=400000 +y_0=0 +ellps=GRS80 +units=m +no_defs "
#proj4 = "+proj=larr +datum=WGS84 +lon_0=0 +lat_ts=45 +x_0=0 +y_0=0 +ellps=WGS84 +units=m +no_defs"
#proj4 = "+proj=nsper +datum=WGS84 +ellps=WGS84 +lon_0=-60 +lat_0=40 +h=2000000000000000000000000"



###########################
# From OGC WKT
print("--------")
print("Testing from ogc wkt:")
print("")
for wkt in sourcestrings("ogcwkt"):
    
    # test parsing
    try:
        print("From:\n")
        print(wkt)
        print("")
        crs = pycrs.parser.from_ogc_wkt(wkt)
        # test outputs
        testoutputs(crs)
        
    except:
        print(traceback.format_exc()+"\n")   

#render_world(crs)




###########################
# From PROJ4
print("--------")
print("Testing from proj4:")
print("")
proj4 = "+proj=robin +lon_0=0 +x_0=0 +y_0=0 +ellps=WGS84 +datum=WGS84 +units=m +no_defs"
print(proj4)
print("")

crs = pycrs.parser.from_proj4(proj4)
testoutputs(crs)

#render_world(crs)




###########################
# From ESRI WKT/PRJ FILE
print("--------")
print("Testing from esri prj file:")
print("")
wkt = open("testfiles/natearth.prj").read()
print(wkt)
print("")

crs = pycrs.loader.from_file("testfiles/natearth.prj")
testoutputs(crs)

#render_world(crs)




