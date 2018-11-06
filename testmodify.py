import pycrs
import traceback
import logging



###########################
# Drawing routine for testing
raw = None
def render_world(crs, savename):
    import urllib2
    import json
    import pygeoj
    import pyagg
    import pyproj
    import random

    # load world borders
    global raw
    if not raw:
        raw = urllib2.urlopen("https://raw.githubusercontent.com/johan/world.geo.json/master/countries.geo.json").read()
    rawdict = json.loads(raw)
    data = pygeoj.load(data=rawdict)

    # convert coordinates
    fromproj = pyproj.Proj("+init=EPSG:4326")
    toproj = pyproj.Proj(crs.to_proj4())
    for feat in data:
        #if feat.properties['name'] != 'United States of America': continue
        if feat.geometry.type == "Polygon":
            feat.geometry.coordinates = [zip(*pyproj.transform(fromproj, toproj, zip(*ring)[0], zip(*ring)[1]))
                                         for ring in feat.geometry.coordinates]
        elif feat.geometry.type == "MultiPolygon":
            feat.geometry.coordinates = [
                                        [zip(*pyproj.transform(fromproj, toproj, zip(*ring)[0], zip(*ring)[1]))
                                         for ring in poly]
                                         for poly in feat.geometry.coordinates]
        feat.geometry.update_bbox() # important to clear away old bbox
    # get zoom area
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
    c = pyagg.Canvas(1000,1000)
    c.geographic_space()
    c.zoom_bbox(*bbox)
    #c.zoom_out(1.3)

    # draw countries
    for feat in data:
        try: c.draw_geojson(feat.geometry,
                            fillcolor="blue",
                            outlinecolor="white")
        except:
            # NOTE: feat.__geo_interface__ is one level too high maybe??
            print("unable to draw?", feat.geometry)

    # draw text of the proj4 string used
    #c.percent_space()
    #c.draw_text(crs.to_proj4(), (50,10))

    # save
    c.save("testrenders/"+savename+".png")





import pyproj
fromproj = pyproj.Proj("+init=EPSG:4326")
x,y = -76.7075, 37.2707

# Load
crs = pycrs.parser.from_esri_code(54030) # Robinson projection from esri code
render_world(crs, 'docs_orig')
print pyproj.transform(fromproj, pyproj.Proj(crs.to_proj4()), x,y)

# Tweak1
crs.toplevel.geogcs.datum = pycrs.elements.datums.NAD83()
#crs.toplevel.geogcs.datum.ellips = pycrs.elements.ellipsoids.WGS72()
render_world(crs, 'docs_tweak1')
print pyproj.transform(fromproj, pyproj.Proj(crs.to_proj4()), x,y)

# Tweak2
crs.toplevel.geogcs.prime_mer.value = 160.0
render_world(crs, 'docs_tweak2')
print pyproj.transform(fromproj, pyproj.Proj(crs.to_proj4()), x,y)

# Tweak3
crs.toplevel.proj = pycrs.elements.projections.Sinusoidal()
render_world(crs, 'docs_tweak3')
print pyproj.transform(fromproj, pyproj.Proj(crs.to_proj4()), x,y)







