import pycrs

###########################
# OGC WKT

crs = pycrs.parser.from_esri_code(54030)
wkt = crs.to_ogc_wkt()
print pycrs.parser.from_ogc_wkt(wkt)



dssdfsd

###########################
# PROJ4

proj4 = "+proj=robin +lon_0=0 +x_0=0 +y_0=0 +ellps=WGS84 +datum=WGS84 +units=m +no_defs"
#proj4 = "+proj=longlat +ellps=WGS84 +datum=WGS84"
#proj4 = "+proj=aea +lat_1=24 +lat_2=31.5 +lat_0=24 +lon_0=-84 +x_0=400000 +y_0=0 +ellps=GRS80 +units=m +no_defs "
proj4 = "+proj=larr +datum=WGS84 +lon_0=0 +lat_ts=45 +x_0=0 +y_0=0 +ellps=WGS84 +units=m +no_defs"
proj4 = "+proj=nsper +datum=WGS84 +ellps=WGS84 +lon_0=44 +lat_0=30 +h=200000000"

#crs = pycrs.parser.from_esri_code(54030)
#crs = pycrs.parser.from_sr_code(7898)
#crs = pycrs.parser.from_epsg_code(4324)
#crs = pycrs.parser.from_sr_code(6618)
crs = pycrs.parser.from_proj4(proj4)

print crs.to_proj4()





import urllib2
import json
import pygeoj
import pyagg
import pyproj
import random
c = pyagg.Canvas(600,600)
c.geographic_space()
raw = urllib2.urlopen("https://raw.githubusercontent.com/johan/world.geo.json/master/countries.geo.json").read()
rawdict = json.loads(raw)
data = pygeoj.load(data=rawdict)
proj4 = crs.to_proj4()
fromproj = pyproj.Proj("+init=EPSG:4326")
toproj = pyproj.Proj(proj4)

print data.bbox
for feat in data:
    if feat.geometry.type == "Polygon":
        feat.geometry.coordinates = [zip(*pyproj.transform(fromproj, toproj, zip(*ring)[0], zip(*ring)[1]))
                                     for ring in feat.geometry.coordinates]
    elif feat.geometry.type == "MultiPolygon":
        feat.geometry.coordinates = [
                                    [zip(*pyproj.transform(fromproj, toproj, zip(*ring)[0], zip(*ring)[1]))
                                     for ring in poly]
                                     for poly in feat.geometry.coordinates]
data.add_all_bboxes()
xmins, ymins, xmaxs, ymaxs = zip(*(feat.geometry.bbox for feat in data))
bbox = (min(xmins), min(ymins), 33333, 33333) # to avoid inf bounds and no render
# print data.bbox #PYGEOJ data.bbox doesnt update.........FIX!
print bbox
c.zoom_bbox(*bbox)
for feat in data:
    try: c.draw_geojson(feat.geometry,
                        fillcolor=tuple(random.randrange(255) for _ in range(3)),
                        outlinecolor="white")
    except:
        # NOTE: feat.__geo_interface__ is one level too high maybe??
        print feat.geometry
c.view()
