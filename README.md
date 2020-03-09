# PyCRS

[![Build Status](https://travis-ci.org/karimbahgat/PyCRS.svg?branch=master)](https://travis-ci.org/karimbahgat/PyCRS)

PyCRS is a pure Python GIS package for reading, writing, and converting between various
common coordinate reference system (CRS) string and data source formats. 

![](https://github.com/karimbahgat/pycrs/raw/master/testrenders/logo.png "PyCRS")

- [GitHub Repository](http://github.com/karimbahgat/PyCRS)
- [API Documentation](https://karimbahgat.github.io/PyCRS/)


## Table of Contents

- [Introduction](#introduction)
- [Status](#status)
- [Changes](#changes)
- [Dependencies](#dependencies)
- [Installation](#installation)
- [Examples](#examples)
    - [Creating a CS Instance](#creating-a-cs-instance)
        - [Loading from an external source](#loading-from-an-external-source)
            - [Loading from a Shapefile](#loading-from-a-shapefile)
            - [Loading from a GeoJSON](#loading-from-a-geojson)
            - [Loading from a URL](#loading-from-a-url)
        - [Parsing from a text string](#parsing-from-a-text-string)
            - [Parsing from proj4 string](#parsing-from-proj4-string)
            - [Parsing from ESRI WKT string](#parsing-from-esri-wkt-string)
            - [Parsing from OGC WKT string](#parsing-from-ogc-wkt-string)
            - [Parsing from unknown string](#parsing-from-unknown-string)
        - [Looking up a coordinate system code](#looking-up-a-coordinate-system-code)
            - [Looking up EPSG codes](#looking-up-epsg-codes)
            - [Looking up ESRI codes](#looking-up-esri-codes)
            - [Looking up SR codes](#looking-up-sr-codes)
		- [Searching for coordinate systems by name or area](#searching-for-coordinate-systems-by-name-or-area)
			- [Loading from search results](#loading-from-search-results)
    - [Inspecting the CS Instance](#inspecting-the-cs-instance)
        - [Geographic CS](#geographic-crs)
        - [Projected CS](#projected-crs)
    - [Converting to other CRS formats](#converting-to-other-crs-formats)
        - [Converting to Proj4](#converting-to-proj4)
        - [Converting to ESRI WKT](#converting-to-esri-wkt)
        - [Converting to OGC WKT](#converting-to-ogc-wkt)
	- [Representing as a coordinate system code](#representing-as-a-coordinate-system-code)
		- [Representing as an EPSG code](#representing-as-an-epsg-code)
- [Recipes](#recipes)
	- [Modifying the CS Instance](#modifying-the-cs-instance)
    - [Coordinate Transformations](#coordinate-transformations)
    - [Writing a Shapefile .prj file](#writing-a-shapefile-.prj-file)
- [Testing](#testing)
- [License](#license)
- [Credits](#credits)


## Introduction

Python should have a standalone GIS library focused solely on coordinate reference system metadata.
That is, a library focused on the various formats used to store and represent crs definitions, including
OGC WKT, ESRI WKT, Proj4, and various short-codes defined by organizations like EPSG, ESRI, and SR-ORG.
Correctly parsing and converting between these formats is essential in many types of GIS work.
For instance when trying to use PyProj to transform coordinates from a non-proj4 crs format. Or
when wanting to convert the crs from a GeoJSON file to a .prj file. Or when simply adding a crs definition
to a file that was previously missing one. 

When I created PyCRS, the only way to read and convert between crs formats was to use the extensive Python
GDAL suite and its srs submodule, but the requirements of some applications might exclude the use of
GDAL. There have also been some online websites/services, but these only allow partial lookups or
one-way conversion from one format to another. I therefore hope that PyCRS will make it easier for
lightweight applications to read a broader range of data files and correctly interpret and possibly transform
their crs definitions. Written entirely in Python I also hope it will help clarify the differences
between the various formats, and make it easier for more people to help keep it up-to-date and bug-free. 


## Status

Currently, the supported formats are OGC WKT (v1), ESRI WKT, Proj4, and any EPSG, ESRI, or SR-ORG code
available from spatialreference.org. In the future I hope to add support for OGC URN identifier strings,
and GeoTIFF file tags.

There are still some cases where PyCRS does not perfectly parse or convert between all crs formats,
based on (hopefully mostly cosmetic) differences from the results of other parsers like GDAL.
In the source repository there is a tester.py script, which uses a barrage of commonly
used crs as listed on http://www.remotesensing.org/geotiff/proj_list/. Currently, the overall success rate
for loading as well as converting between the three main formats is 80-90%, and visual inspections of 
rendering the world with each crs generally look correct. However, whether the converted crs strings
are logically equivalent to each other from a mathematical standpoint is something that needs a more detailed
quality check. 


## Changes

### 1.0.2 (2020-03-09)

- Add search functions to lookup epsg.io
- Add to_epsg_code() method from, based on prj2epsg.org (#47, @fitoprincipe)
- Switch to using epsg.io when looking up epsg codes
- Fix broken spatialreference link by switching to SSL
- Added Clarke 1880 ellipsoid
- Use default datum ellipsoid when ellipsoid not specified
- Better warning and error when proj4 ellipsoid cannot be found
- Misc bug fixes

### 1.0.1 (2019-03-07)

- Misc docstring changes
- More flexible parsing, in case projection is not the second element
- More informative exceptions

### 1.0.0 (2019-02-04)

- API Changes:
- Dropping CRS wrapper class, instead handling GeogCS or ProjCS directly
- Change module names to load.py, and parse.py
- Move Ellipsoid, Datum, and Projection to their respective modules
- Allow proj4 input and output as dict
- Fixes:
- Added more documentation
- Fix +f interpretation
- Include reading +rf parameter
- Better ellipsoid support for +a and +b
- Fix Python 3 bugs
- Fix proj4 standard parallels being ignored
- Parse WKT CS names which were ignored before
- Support for prime meridian city names

### 0.1.3 (2016-06-25)

- Fixed various bugs
- Pip install fix for Mac and Linux
- Python 3 compatability

### 0.1.2 (2015-08-05)

- First official release


## Dependencies

Pure Python, no dependencies. Python 2 and 3 compatible. 


## Installation

PyCRS is installed with pip from the commandline:

    pip install pycrs

It also works to just place the "pycrs" package folder in an importable location like 
"PythonXX/Lib/site-packages".


## Examples

Begin by importing the pycrs module:

    >>> import pycrs


### Creating a CS Instance

PyCRS uses different types of CS classes to represent and handle all coordinate reference systems.
To create one you can either load it from a source, parse it from a string,
look up from a CRS code, or build it from scratch. Let's review these different ways of creating
a CS type instance. 


#### Loading from an external source

If you know the crs information is located in some external source, PyCRS provides some convenient
functions for loading these, all located in the "pycrs.load" module. 

##### Loading from a Shapefile

In most situations this will mean reading the ESRI .prj file that accomponies
a shapefile. PyCRS has a convenience function for doing that:

    >>> crs = pycrs.load.from_file("testfiles/natearth.prj")

##### Loading from a GeoJSON

The same function also supports reading the crs from GeoJSON files:

    >>> crs = pycrs.load.from_file("testfiles/cshapes.geo.json")

##### Loading from a URL

If your crs is not defined in a file, but rather as plain text on a webpage, there is also a function for that:

    >>> crs = pycrs.load.from_url("http://spatialreference.org/ref/esri/54030/ogcwkt/")


#### Parsing from a text string

In many cases however, you may already have the string representation in your code. This could be if you
are interoperating with other libraries, or you have already read it from some external source.
In these cases, you can create the CS type instance by using the functions available in the "pycrs.parse"
module.

##### Parsing from proj4 string or dict

To create the CS type instance from a proj4 string, you can do like this:

    >>> proj4 = "+proj=robin +lon_0=0 +x_0=0 +y_0=0 +ellps=WGS84 +datum=WGS84 +units=m +no_defs"
    >>> crs = pycrs.parse.from_proj4(proj4)

Or if your proj4 string is represented as a dict:

    >>> proj4_as_dict = dict(proj='robin', lon_0=0, x_0=0, y_0=0, ellps='WGS84', datum='WGS84', units='m')
    >>> crs = pycrs.parse.from_proj4(proj4_as_dict)

##### Parsing from ESRI WKT string

The ESRI WKT format is the format typically found in a shapefile's .prj file.
If you have already loaded it from a file, you can parse it like this:

    >>> esri_wkt = 'PROJCS["World_Robinson",GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137,298.257223563]],PRIMEM["Greenwich",0],UNIT["Degree",0.017453292519943295]],PROJECTION["Robinson"],PARAMETER["False_Easting",0],PARAMETER["False_Northing",0],PARAMETER["Central_Meridian",0],UNIT["Meter",1]]'
    >>> crs = pycrs.parse.from_esri_wkt(esri_wkt)

##### Parsing from OGC WKT string

The Open Geospatial Consortium (OGC) WKT format is a newer variant of the ESRI WKT.
There are only minor differences, but will likely be more supported in the future. 
If you already have it as a string, you can parse it like this:

    >>> ogc_wkt = 'PROJCS["World_Robinson",GEOGCS["GCS_WGS_1984",DATUM["WGS_1984",SPHEROID["WGS_1984",6378137,298.257223563]],PRIMEM["Greenwich",0],UNIT["Degree",0.017453292519943295]],PROJECTION["Robinson"],PARAMETER["False_Easting",0],PARAMETER["False_Northing",0],PARAMETER["Central_Meridian",0],UNIT["Meter",1],AUTHORITY["EPSG","54030"]]'
    >>> crs = pycrs.parse.from_ogc_wkt(ogc_wkt)

##### Parsing from unknown string

Finally, if you do not know the format of the crs string, you can also let PyCRS autodetect
and parse the crs type for you:

    >>> for unknown in [proj4, esri_wkt, ogc_wkt]:
    ...     crs = pycrs.parse.from_unknown_text(unknown)


#### Looking up a coordinate system code

Another common way to store a coordinate system is through a lookup code that is available for
many of the more commonly used ones. Multiple different agencies have defined their own sets of
codes.

##### Looking up EPSG codes

To look up codes defined by EPSG:

    >>> crs = pycrs.parse.from_epsg_code(4326)

##### Looking up ESRI codes

To look up codes defined by ESRI:

    >>> crs = pycrs.parse.from_esri_code(54030)

##### Looking up SR codes

To look up codes defined by spatialreference.org:

    >>> crs = pycrs.parse.from_sr_code(42)
	

#### Searching for coordinate systems by name or area

Finally, if you don't know the specific code or definition of a particular crs there's also search functions to look it up on the epsg.io website. For instance, if you want to use the Robinson projection but not sure how to load it, you could interactively search and inspect the potential matches: 

	>>> for match in pycrs.utils.search_name('robinson'): 
	...     # do something
	... 	pass
	
Similarly, if you need to know which projection would be suitable for a particular country, you could search for that as well:
    
	>>> for match in pycrs.utils.search_area('brazil'): 
	...     # do something
	... 	pass
	
You could also do a custom search using various specifiers, such as a projection in a particular area (the full list of specifiers is available at https://github.com/maptiler/epsg.io):

	>>> for match in pycrs.utils.search('name:utm area:belgium'): 
	... 	# do something
	... 	pass
	
##### Loading from search results
	
The search match results include the epsg code, proj4, and wkt representations, any of which could be used to load a CS instance: 

	>>> topmatch = next(pycrs.utils.search_name('wgs 84'))
	>>> crs = pycrs.parse.from_proj4(topmatch['proj4'])
	


### Inspecting the CS Instance

Once you have loaded, parsed, looked up, or created a coordinate reference system, you end up with one of the 
CS type instances in the pycrs.cs module. All CS types are subclasses of pycrs.CS:

	>>> isinstance(crs, pycrs.CS)
	True
	
PyCRS currently only supports the two most common types of CS, geographic or projected. 

#### Geographic CS

A geographic reference system keeps coordinates in the latitude-longitude space, and the reason we specify
it is because there are different ways of defining the shape of the earth. As an example, let's load the commonly
used WGS84 geographic coordinate system:

    >>> crs = pycrs.parse.from_epsg_code(4326)
	
If it loaded correctly you should now have a pycrs.GeogCS instance, which you can also check through the `cs_type` attribute:

	>>> isinstance(crs, pycrs.GeogCS)
	True
    >>> crs.cs_type
    'Geographic'

Through the GeogCS instance, we can further access its subcomponents and parameters.
For instance, if we wanted to check the datum we could do:

    >>> datum = crs.datum
    >>> isinstance(datum, pycrs.elements.datums.WGS84)
    True

Or the inverse flattening factor of the ellipsoid:

    >>> ellips = crs.datum.ellips
    >>> ellips.inv_flat.value
    298.257223563

For more ideas on how to inspect the GeogCS instance, the following overview gives an idea of the
composition and attributes of a geographic CS:

- pycrs.GeogCS
	- `name` -> string
	- `datum` -> a datum from pycrs.elements.datums
		- `name` -> pycrs.elements.datums.DatumName
			- `proj4` -> string
			- `esri_wkt` -> string
			- `ogc_wkt` -> string
		- `ellips` -> an ellipsoid from pycrs.elements.ellipsoids
			- `name` -> pycrs.elements.ellipsoids.EllipsoidName
				- `proj4` -> string
				- `esri_wkt` -> string
				- `ogc_wkt` -> string
			- `semimaj_ax` -> pycrs.elements.parameters.SemiMajorRadius
				- `value` -> float
			- `semimin_ax` -> (optional) pycrs.elements.parameters.SemiMinorRadius
				- `value` -> float
			- `flat` -> (optional) pycrs.elements.parameters.Flattening
				- `value` -> float
			- `inv_flat` -> (optional) pycrs.elements.parameters.InverseFlattening
				- `value` -> float
		- `datumshift` -> (optional) pycrs.elements.parameters.DatumShift or None
	- `prime_mer` -> pycrs.elements.parameters.PrimeMeridian
		- `value` -> float
	- `angunit` -> an angular unit from pycrs.elements.units, eg Degree
		- `unitname` -> pycrs.elements.units.UnitName
			- `proj4` -> string
			- `esri_wkt` -> string
			- `ogc_wkt` -> string
		- `unitmultiplier` -> pycrs.elements.units.UnitMultiplier
			- `value` -> float
	- `twin_ax` -> tuple
		- 1: a named compass direction (east-west) from pycrs.elements.directions
		- 2: a named compass direction (north-south) from pycrs.elements.directions

#### Projected CS

A projected reference system keeps coordinates in projected x-y space. In addition to
defining the shape of the earth through a child GeogCS, the projected reference system
defines some additional parameters in order to transform the coordinates to a wide
variety of map types. Let's take the commonly used World Robinson projected coordinate
system as our example:

    >>> crs = pycrs.parse.from_esri_code(54030)
	
If it loaded correctly you should now have a pycrs.ProjCS instance, which you can also check through the `cs_type` attribute:

	>>> isinstance(crs, pycrs.ProjCS)
	True
    >>> crs.cs_type
    'Projected'

Through the ProjCS instance, we can further access its subcomponents and parameters.
For instance, if we wanted to check the named projection we could do:

    >>> proj = crs.proj
    >>> isinstance(proj, pycrs.elements.projections.Robinson)
    True

Or check the type of coordinate unit:

    >>> unit = crs.unit
    >>> isinstance(unit, pycrs.elements.units.Meter)
    True

For more ideas on how to inspect the ProjCS instance, the following overview gives an idea of the
composition and attributes of a projected CS:

- pycrs.ProjCS
	- `name` -> string
	- `geogcs` -> pycrs.GeogCS (See the section on geographic CS...)
	- `proj` -> a projection from pycrs.elements.projections
		- `name` -> pycrs.elements.projections.ProjName
			- `proj4` -> string
			- `esri_wkt` -> string
			- `ogc_wkt` -> string
	- `params` -> list
		- 1: named parameters from pycrs.elements.parameters
		- 2: named parameters from pycrs.elements.parameters
		- 3: ...
		- n: named parameters from pycrs.elements.parameters
	- `unit` -> a unit from pycrs.elements.units
		- `unitname` -> pycrs.elements.units.UnitName
			- `proj4` -> string
			- `esri_wkt` -> string
			- `ogc_wkt` -> string
		- `unitmultiplier` -> pycrs.elements.units.UnitMultiplier
			- `value` -> float
	- `twin_ax` -> tuple
		- 1: a named compass direction (east-west) from pycrs.elements.directions
		- 2: a named compass direction (north-south) from pycrs.elements.directions

    

### Converting to other CRS formats

Once you have read the crs of the original data source, you may want to convert it to some other crs format.
PyCRS allows converting to the following CRS formats:

#### Converting to Proj4

	# as a string
    >>> crs.to_proj4()
    '+proj=robin +datum=WGS84 +ellps=WGS84 +a=6378137.0 +rf=298.257223563 +pm=0 +lon_0=0 +x_0=0 +y_0=0 +units=m +axis=enu +no_defs'
	
	# or as a dict
	>>> isinstance(crs.to_proj4(as_dict=True), dict)
	True

#### Converting to ESRI WKT

    >>> crs.to_esri_wkt()
    'PROJCS["Unknown", GEOGCS["Unknown", DATUM["D_WGS_1984", SPHEROID["WGS_1984", 6378137.0, 298.257223563]], PRIMEM["Greenwich", 0], UNIT["Degree", 0.017453292519943295], AXIS["Lon", EAST], AXIS["Lat", NORTH]], PROJECTION["Robinson"], PARAMETER["Central_Meridian", 0], PARAMETER["False_Easting", 0], PARAMETER["False_Northing", 0], UNIT["Meter", 1.0], AXIS["X", EAST], AXIS["Y", NORTH]]'

#### Converting to OGC WKT

    >>> crs.to_ogc_wkt()
    'PROJCS["Unknown", GEOGCS["Unknown", DATUM["WGS_1984", SPHEROID["WGS_1984", 6378137.0, 298.257223563]], PRIMEM["Greenwich", 0], UNIT["degree", 0.017453292519943295], AXIS["Lon", EAST], AXIS["Lat", NORTH]], PROJECTION["Robinson"], PARAMETER["Central_Meridian", 0], PARAMETER["false_easting", 0], PARAMETER["false_northing", 0], UNIT["Meters", 1.0], AXIS["X", EAST], AXIS["Y", NORTH]]'
	
	
### Representing as a coordinate system code

Just as it's possible to load the crs from predefined coordinate system codes defined by various authorities, it's also sometimes needed to lookup and represent the crs as a coordinate system code, if it exists. 

#### Representing as an EPSG code

Currently, this is only implemented for looking up the EPSG code. This searches the crs wkt representation on prj2epsg.org and returns the EPSG code of the first result, or None if the wkt does not have an associated EPSG code. 

	# to epsg code
	>>> crs = pycrs.parse.from_epsg_code(4326)
	>>> crs.to_epsg_code()
	4326
	
Because a crs definition can have many variations, looking up its coordinate system code might yield multiple possible matches, in which case a warning is raised. For more control to choose the right match, a wkt search utility is also available that returns all possible matches with metadata: 

	# more flexible utility search for epsg code
	>>> crs = pycrs.parse.from_sr_code(42)
	>>> results = pycrs.utils.wkt_to_epsg(crs.to_esri_wkt())
	
	# display the top match info
	>>> topmatch = results['codes'][0]
	>>> topmatch['code']
	'3857'
	>>> topmatch['name']
	'WGS 84 / Pseudo-Mercator'


---
	
## Recipes

### Modifying the CS Instance

In most case you will only ever need to load a CRS and convert it to some format. 
Sometimes, however, you may want to tweak the parameters of your CS type instance.
Knowing the composition of your CS type instance, this is as easy as setting/replacing the
desired attributes. 

Let's demonstrate some examples using the World Robinson projection:

    >>> crs = pycrs.parse.from_esri_code(54030) # Robinson projection from esri code
    >>> crs.to_ogc_wkt()
    'PROJCS["Unknown", GEOGCS["Unknown", DATUM["WGS_1984", SPHEROID["WGS_1984", 6378137.0, 298.257223563]], PRIMEM["Greenwich", 0], UNIT["degree", 0.017453292519943295], AXIS["Lon", EAST], AXIS["Lat", NORTH]], PROJECTION["Robinson"], PARAMETER["Central_Meridian", 0], PARAMETER["false_easting", 0], PARAMETER["false_northing", 0], UNIT["Meters", 1.0], AXIS["X", EAST], AXIS["Y", NORTH]]'

Here is a map of the default Robinson projection:

![](https://github.com/karimbahgat/pycrs/raw/master/testrenders/docs_orig.png "Defualt Robinson")

Let's say we wanted to switch its datum from WGS84 to NAD83, we could do it
like so:

    >>> crs.geogcs.datum = pycrs.elements.datums.NAD83()
    >>> crs.to_ogc_wkt()
    'PROJCS["Unknown", GEOGCS["Unknown", DATUM["North_American_Datum_1983", SPHEROID["GRS_1980", 6378137.0, 298.257222101]], PRIMEM["Greenwich", 0], UNIT["degree", 0.017453292519943295], AXIS["Lon", EAST], AXIS["Lat", NORTH]], PROJECTION["Robinson"], PARAMETER["Central_Meridian", 0], PARAMETER["false_easting", 0], PARAMETER["false_northing", 0], UNIT["Meters", 1.0], AXIS["X", EAST], AXIS["Y", NORTH]]'

Or let's say we wanted to switch its prime meridian, so that the longitude axis is centered
closer to the Pacific instead of over Greenwhich:

    >>> crs.geogcs.prime_mer.value = 160.0
    >>> crs.to_ogc_wkt()
    'PROJCS["Unknown", GEOGCS["Unknown", DATUM["North_American_Datum_1983", SPHEROID["GRS_1980", 6378137.0, 298.257222101]], PRIMEM["Greenwich", 160], UNIT["degree", 0.017453292519943295], AXIS["Lon", EAST], AXIS["Lat", NORTH]], PROJECTION["Robinson"], PARAMETER["Central_Meridian", 0], PARAMETER["false_easting", 0], PARAMETER["false_northing", 0], UNIT["Meters", 1.0], AXIS["X", EAST], AXIS["Y", NORTH]]'

And here is what that map would look like (the odd-looking lines is just a rendering issue due to
polygons that cross the meridian):

![](https://github.com/karimbahgat/pycrs/raw/master/testrenders/docs_tweak2.png "Modified Robinson")

Or if we just switch the projection type alltogether:

    >>> crs.proj = pycrs.elements.projections.Sinusoidal()
    >>> crs.to_ogc_wkt()
    'PROJCS["Unknown", GEOGCS["Unknown", DATUM["North_American_Datum_1983", SPHEROID["GRS_1980", 6378137.0, 298.257222101]], PRIMEM["Greenwich", 160], UNIT["degree", 0.017453292519943295], AXIS["Lon", EAST], AXIS["Lat", NORTH]], PROJECTION["Sinusoidal"], PARAMETER["Central_Meridian", 0], PARAMETER["false_easting", 0], PARAMETER["false_northing", 0], UNIT["Meters", 1.0], AXIS["X", EAST], AXIS["Y", NORTH]]'
	
![](https://github.com/karimbahgat/pycrs/raw/master/testrenders/docs_tweak3.png "Modified Sinusoidal")	

### Coordinate Transformations

A common reason for wanting to convert between CRS formats, is if you want to transform coordinates
from one coordinate system to another. In Python this is typically done with the PyProj module,
which only takes proj4 format. Using PyCRS we can easily define the original coordinate system that
we want to convert and get its proj4 representation:

    >>> fromcrs = pycrs.parse.from_epsg_code(4326) # WGS84 projection from epsg code
    >>> fromcrs_proj4 = fromcrs.to_proj4()

We can then use PyCRS to define our target projection from the format of your choice, before converting
it to the proj4 format that PyProj expects:

    >>> tocrs = pycrs.parse.from_esri_code(54030) # Robinson projection from esri code
    >>> tocrs_proj4 = tocrs.to_proj4()

With the source and target projections defined in the proj4 crs format, we are ready to transform our
data coordinates with PyProj: 

    >>> import pyproj
    >>> fromproj = pyproj.Proj(fromcrs_proj4)
    >>> toproj = pyproj.Proj(tocrs_proj4)
    >>> lng,lat = -76.7075, 37.2707  # Williamsburg, Virginia :)
    >>> pyproj.transform(fromproj, toproj, lng, lat)
    (-6766170.001635834, 3985755.032695593)

### Writing a Shapefile .prj file

After you transform your data coordinates you may also wish to save the data back to file along with the new
crs. With PyCRS you can do this in a variety of crs format. For instance, to write a shapefile .prj file:

    >>> with open("testfiles/shapefile.prj", "w") as writer:
    ...     _ = writer.write(tocrs.to_esri_wkt())



---

## Testing

The testing suite is still a work in progress and is spread across multiple files.
The files testdocs.py (the official doctests) and testbatch.py (tests and renders a batch of projections)
can be run from the prompt:

    python testdocs.py
    python testbatch.py

The test files have a few dependent python packages that will need to be installed to fully work:

- [pyproj](https://github.com/jswhit/pyproj) - cartographic projection and coordinate system transformation, python wrapper PROJ.4 C library
- [PyAgg](https://github.com/karimbahgat/PyAgg) - Aggdraw wrapper for lightweight drawing
- [PyGeoj](https://github.com/karimbahgat/PyGeoj) - geojson reader/writer
 






## License

This code is free to share, use, reuse,
and modify according to the MIT license, see license.txt



## Credits

- Karim Bahgat
- Micah Cochrain
- Mike Kittridge
- Roger Lew
- Gregory Halvorsen
- M Clark
- David Hoese
- Rodrigo E. Principe
