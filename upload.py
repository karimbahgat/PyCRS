import pipy
 
packpath = "pycrs"
pipy.define_upload(packpath,
                   author="Karim Bahgat",
                   author_email="karim.bahgat.norway@gmail.com",
                   license="MIT",
                   name="PyCRS",
                   changes=['Add search functions to lookup epsg.io',
                            'Add to_epsg_code() method from, based on prj2epsg.org (#47, @fitoprincipe)',
                            'Switch to using epsg.io when looking up epsg codes',
                            'Fix broken spatialreference link by switching to SSL',
                            'Added Clarke 1880 ellipsoid',
                            'Use default datum ellipsoid when ellipsoid not specified',
                            'Better warning and error when proj4 ellipsoid cannot be found',
                            'Misc bug fixes'],
                   description="GIS package for reading, writing, and converting between CRS formats.",
                   url="http://github.com/karimbahgat/PyCRS",
                   keywords="GIS spatial CRS projection coordinate system format",
                   classifiers=["License :: OSI Approved",
                                "Programming Language :: Python",
                                "Development Status :: 5 - Production/Stable",
                                "Intended Audience :: Developers",
                                "Intended Audience :: Science/Research",
                                'Intended Audience :: End Users/Desktop',
                                "Topic :: Scientific/Engineering :: GIS"],
                   )

pipy.generate_docs(packpath)
#pipy.upload_test(packpath)
#pipy.upload(packpath)

