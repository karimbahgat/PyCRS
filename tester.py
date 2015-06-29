import pycrs

proj4 = "+proj=robin +lon_0=0 +x_0=0 +y_0=0 +ellps=WGS84 +datum=WGS84 +units=m +no_defs"
proj4 = "+proj=longlat +ellps=WGS84 +datum=WGS84"

crs = pycrs.parser.from_proj4(proj4)

print crs.to_ogc_wkt()


