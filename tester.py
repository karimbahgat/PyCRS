import pycrs
import traceback
import logging



###########################
# Drawing routine for testing
def render_world(crs, savename):
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
    c.zoom_out(1.3)

    # draw countries
    for feat in data:
        try: c.draw_geojson(feat.geometry,
                            fillcolor=tuple(random.randrange(255) for _ in range(3)),
                            outlinecolor="white")
        except:
            # NOTE: feat.__geo_interface__ is one level too high maybe??
            print("unable to draw?", feat.geometry)

    # draw text of the proj4 string used
    c.percent_space()
    c.draw_text(crs.to_proj4(), (50,10))

    # save
    c.save("testrenders/"+savename+".png")






# Source string generator
def sourcestrings(format):
    # commonly used projections on global scale
    # from http://www.remotesensing.org/geotiff/proj_list/
    
    ##Albers Equal-Area Conic
    yield pycrs.utils.crscode_to_string("sr-org", 62, format)
    ##Azimuthal Equidistant
    yield pycrs.utils.crscode_to_string("esri", 54032, format)
    ##Cassini-Soldner
    # ...ignore, too specific
    ##Cylindrical Equal Area
    yield pycrs.utils.crscode_to_string("sr-org", 8287, format)
    ##Eckert IV
    yield pycrs.utils.crscode_to_string("esri", 54012, format)
    ##Eckert VI
    yield pycrs.utils.crscode_to_string("esri", 54010, format)
    ##Equidistant Conic
    yield pycrs.utils.crscode_to_string("esri", 54027, format)
    ##Equidistant Cylindrical
    yield pycrs.utils.crscode_to_string("epsg", 3786, format)
    ##Equirectangular
    yield pycrs.utils.crscode_to_string("sr-org", 8270, format)
    ##Gauss-Kruger
    # ...not found???
    ##Gall Stereographic
    yield pycrs.utils.crscode_to_string("esri", 54016, format)
    ##GEOS - Geostationary Satellite View
    yield pycrs.utils.crscode_to_string("sr-org", 81, format)
    ##Gnomonic
    # ...not found
    ##Hotine Oblique Mercator
    yield pycrs.utils.crscode_to_string("esri", 54025, format)
    ##Krovak
    yield pycrs.utils.crscode_to_string("sr-org", 6688, format)
    ##Laborde Oblique Mercator
    # ...not found # yield pycrs.utils.crscode_to_string("epsg", 9813, format)
    ##Lambert Azimuthal Equal Area
    yield pycrs.utils.crscode_to_string("sr-org", 28, format)
    ##Lambert Conic Conformal (1SP)
    # ...not found
    ##Lambert Conic Conformal (2SP)
    yield pycrs.utils.crscode_to_string("sr-org", 29, format) # yield pycrs.utils.crscode_to_string("epsg", 9802, format)
    ##Lambert Conic Conformal (2SP Belgium)
    # ...ignore, too specific
    ##Lambert Cylindrical Equal Area
    yield pycrs.utils.crscode_to_string("sr-org", 8287, format)
    ##Mercator (1SP)
    yield pycrs.utils.crscode_to_string("sr-org", 16, format)
    ##Mercator (2SP)
    yield pycrs.utils.crscode_to_string("sr-org", 7094, format)
    ##Miller Cylindrical
    yield pycrs.utils.crscode_to_string("esri", 54003, format)
    ##Mollweide
    yield pycrs.utils.crscode_to_string("esri", 54009, format)
    ##New Zealand Map Grid
    # ...ignore, too specific
    ##Oblique Mercator
    yield pycrs.utils.crscode_to_string("esri", 54025, format)
    ##Oblique Stereographic
    yield pycrs.utils.crscode_to_string("epsg", 3844, format)
    ##Orthographic
    yield pycrs.utils.crscode_to_string("sr-org", 6980, format)
    ##Polar Stereographic
    yield pycrs.utils.crscode_to_string("sr-org", 8243, format)
    ##Polyconic
    yield pycrs.utils.crscode_to_string("esri", 54021, format)
    ##Robinson
    yield pycrs.utils.crscode_to_string("esri", 54030, format)
    ##Rosenmund Oblique Mercator
    # ...not found
    ##Sinusoidal
    yield pycrs.utils.crscode_to_string("sr-org", 6965, format)
    ##Swiss Oblique Cylindrical
    # ...ignore, too specific
    ##Swiss Oblique Mercator
    # ...ignore, too specific
    ##Stereographic
    yield pycrs.utils.crscode_to_string("sr-org", 6711, format)
    ##Transverse Mercator
    # ...not found???
    ##Transverse Mercator (Modified Alaska)
    # ...ignore, too specific
    ##Transverse Mercator (South Oriented)
    # ...ignore, too specific
    ##Tunisia Mining Grid
    # ...ignore, too specific
    ##VanDerGrinten
    yield pycrs.utils.crscode_to_string("sr-org", 6978, format)
    
    # bunch of randoms
    #yield pycrs.utils.crscode_to_string("esri", 54030, format)
    #yield pycrs.utils.crscode_to_string("sr-org", 7898, format)
    #yield pycrs.utils.crscode_to_string("sr-org", 6978, format)
    #yield pycrs.utils.crscode_to_string("epsg", 4324, format)
    #yield pycrs.utils.crscode_to_string("sr-org", 6618, format)
    #yield pycrs.utils.crscode_to_string("sr-org", 22, format)
    #yield pycrs.utils.crscode_to_string("esri", 54031, format)
    # add more...

    # Misc other crs for testing
    #crs = pycrs.utils.crscode_to_string("esri", 54030, "proj4")
    #crs = pycrs.utils.crscode_to_string("sr-org", 6978, "proj4")
    #crs = pycrs.parser.from_sr_code(7898)
    #crs = pycrs.parser.from_epsg_code(4324)
    #crs = pycrs.parser.from_sr_code(6618)
    #crs = pycrs.parser.from_sr_code(22)
    #crs = pycrs.parser.from_esri_code(54031)
    #proj4 = "+proj=longlat +ellps=WGS84 +datum=WGS84"
    #proj4 = "+proj=aea +lat_1=24 +lat_2=31.5 +lat_0=24 +lon_0=-84 +x_0=400000 +y_0=0 +ellps=GRS80 +units=m +no_defs "
    #proj4 = "+proj=larr +datum=WGS84 +lon_0=0 +lat_ts=45 +x_0=0 +y_0=0 +ellps=WGS84 +units=m +no_defs"
    #proj4 = "+proj=nsper +datum=WGS84 +ellps=WGS84 +lon_0=-60 +lat_0=40 +h=2000000000000000000000000"





# Testing format outputs
def testoutputs(crs):
    print("ogc_wkt:\n")
    try:
        print(crs.to_ogc_wkt()+"\n")
        global ogcwkt_outputs
        ogcwkt_outputs += 1
    except: logging.warn(traceback.format_exc())

    print("esri_wkt:\n")
    try:
        print(crs.to_esri_wkt()+"\n")
        global esriwkt_outputs
        esriwkt_outputs += 1
    except: logging.warn(traceback.format_exc())
          
    print("proj4:\n")
    try:
        print(crs.to_proj4()+"\n")
        global proj4_outputs
        proj4_outputs += 1
    except: logging.warn(traceback.format_exc())





#############################################################################




###########################
# From OGC WKT
print("--------")
print("Testing from ogc wkt:")
print("")

totals = 0
loaded = 0
ogcwkt_outputs = 0
esriwkt_outputs = 0
proj4_outputs = 0
renders = 0

for wkt in sourcestrings("ogcwkt"):
    totals += 1
    
    # test parsing
    try:
        print("From:\n")
        print(wkt)
        print("")
        crs = pycrs.parser.from_ogc_wkt(wkt)
        loaded += 1
        
        # test outputs
        print("To:\n")
        testoutputs(crs)
        
        # test render
        try:
            print("Rendering...")
            savename = "%i_from_ogcwkt" % totals
            render_world(crs, savename)
            renders += 1
            print("Successully rendered! \n")
        except:
            logging.warn(traceback.format_exc()+"\n")

    except:
        logging.warn(traceback.format_exc()+"\n")

print("Summary results:")
print("  Loaded: %f%%" % (loaded/float(totals)*100) )
print("  Outputs (OGC WKT): %f%%" % (ogcwkt_outputs/float(totals)*100) )
print("  Outputs (ESRI WKT): %f%%" % (esriwkt_outputs/float(totals)*100) )
print("  Outputs (Proj4): %f%%" % (proj4_outputs/float(totals)*100) )
print("  Renders: %f%%" % (renders/float(totals)*100) )




###########################
# From PROJ4
print("--------")
print("Testing from proj4:")
print("")

totals = 0
loaded = 0
ogcwkt_outputs = 0
esriwkt_outputs = 0
proj4_outputs = 0
renders = 0

for proj4 in sourcestrings("proj4"):
    totals += 1
    
    # test parsing
    try:
        print("From:\n")
        print(proj4)
        print("")
        crs = pycrs.parser.from_proj4(proj4)
        loaded += 1
        
        # test outputs
        print("To:\n")
        testoutputs(crs)
        
        # test render
        try:
            print("Rendering...")
            savename = "%i_from_proj4" % totals
            render_world(crs, savename)
            renders += 1
            print("Successully rendered! \n")
        except:
            logging.warn(traceback.format_exc()+"\n")

    except:
        logging.warn(traceback.format_exc()+"\n")

print("Summary results:")
print("  Loaded: %f%%" % (loaded/float(totals)*100) )
print("  Outputs (OGC WKT): %f%%" % (ogcwkt_outputs/float(totals)*100) )
print("  Outputs (ESRI WKT): %f%%" % (esriwkt_outputs/float(totals)*100) )
print("  Outputs (Proj4): %f%%" % (proj4_outputs/float(totals)*100) )
print("  Renders: %f%%" % (renders/float(totals)*100) )




###########################
# From ESRI WKT/PRJ FILE
print("--------")
print("Testing from esri wkt:")
print("")

totals = 0
loaded = 0
ogcwkt_outputs = 0
esriwkt_outputs = 0
proj4_outputs = 0
renders = 0

for wkt in sourcestrings("esriwkt"):
    totals += 1
    
    # test parsing
    try:
        print("From:\n")
        print(wkt)
        print("")
        crs = pycrs.parser.from_esri_wkt(wkt)
        loaded += 1
        
        # test outputs
        print("To:\n")
        testoutputs(crs)
        
        # test render
        try:
            print("Rendering...")
            savename = "%i_from_esriwkt" % totals
            render_world(crs, savename)
            renders += 1
            print("Successully rendered! \n")
        except:
            logging.warn(traceback.format_exc()+"\n")

    except:
        logging.warn(traceback.format_exc()+"\n")

print("Summary results:")
print("  Loaded: %f%%" % (loaded/float(totals)*100) )
print("  Outputs (OGC WKT): %f%%" % (ogcwkt_outputs/float(totals)*100) )
print("  Outputs (ESRI WKT): %f%%" % (esriwkt_outputs/float(totals)*100) )
print("  Outputs (Proj4): %f%%" % (proj4_outputs/float(totals)*100) )
print("  Renders: %f%%" % (renders/float(totals)*100) )



