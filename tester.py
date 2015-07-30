import pycrs




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






###########################
# OGC WKT
print("--------")
print("testing ogc wkt")
print("")
#crs = pycrs.parser.from_sr_code(54030)
#crs = pycrs.parser.from_sr_code(22)
#crs = pycrs.parser.from_esri_code(54031)
crs = pycrs.parser.from_sr_code(6978)
wkt = crs.to_ogc_wkt()

print("Original:", wkt)
print("")

crs = pycrs.parser.from_ogc_wkt(wkt)

print("Reconstructed:", crs.to_ogc_wkt())
print("")

#render_world(crs)




###########################
# PROJ4
print("--------")
print("testing proj4")
print("")
proj4 = "+proj=robin +lon_0=0 +x_0=0 +y_0=0 +ellps=WGS84 +datum=WGS84 +units=m +no_defs"
#proj4 = "+proj=longlat +ellps=WGS84 +datum=WGS84"
#proj4 = "+proj=aea +lat_1=24 +lat_2=31.5 +lat_0=24 +lon_0=-84 +x_0=400000 +y_0=0 +ellps=GRS80 +units=m +no_defs "
#proj4 = "+proj=larr +datum=WGS84 +lon_0=0 +lat_ts=45 +x_0=0 +y_0=0 +ellps=WGS84 +units=m +no_defs"
#proj4 = "+proj=nsper +datum=WGS84 +ellps=WGS84 +lon_0=-60 +lat_0=40 +h=2000000000000000000000000"

print("Original:", proj4)
print("")

#crs = pycrs.parser.from_esri_code(54030)
#crs = pycrs.parser.from_sr_code(7898)
#crs = pycrs.parser.from_epsg_code(4324)
#crs = pycrs.parser.from_sr_code(6618)
crs = pycrs.parser.from_proj4(proj4)
#crs = pycrs.parser.from_ogc_wkt(wkt)

print("Reconstructed:", crs.to_proj4())
print("")

#render_world(crs)




###########################
# ESRI WKT/PRJ FILE
print("--------")
print("testing esri prj file")
print("")
crs = pycrs.loader.from_file("testfiles/natearth.prj")
wkt = crs.to_esri_wkt()

print("Original:", wkt)
print("")

crs = pycrs.parser.from_esri_wkt(wkt)

print("Reconstructed:", crs.to_esri_wkt())
print("")

#render_world(crs)




