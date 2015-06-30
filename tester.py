import pycrs

proj4 = "+proj=robin +lon_0=0 +x_0=0 +y_0=0 +ellps=WGS84 +datum=WGS84 +units=m +no_defs"
#proj4 = "+proj=longlat +ellps=WGS84 +datum=WGS84"


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
data.add_all_bboxes()
xmins, ymins, xmaxs, ymaxs = zip(*(feat.geometry.bbox for feat in data))
bbox = (min(xmins), min(ymins), max(xmaxs), max(ymaxs))
# print data.bbox #PYGEOJ data.bbox doesnt update.........FIX!
print bbox
c.zoom_bbox(*bbox)
for feat in data:
    if feat.geometry.type == "Polygon":
        try: c.draw_geojson(feat.geometry, outlinecolor="white")
        except:
            # NOTE: feat.__geo_interface__ is one level too high maybe??
            print feat.geometry
c.view()
