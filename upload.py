import pipy
 
packpath = "pycrs"
pipy.define_upload(packpath,
                   author="Karim Bahgat",
                   author_email="karim.bahgat.norway@gmail.com",
                   license="MIT",
                   name="PyCRS",
                   changes=["Fixed various bugs",
                            "Pip install fix for Mac and Linux",
                            "Python 3 compatability"],
                   description="GIS package for reading, writing, and converting between CRS formats.",
                   url="http://github.com/karimbahgat/PyCRS",
                   keywords="GIS spatial CRS coordinates format",
                   classifiers=["License :: OSI Approved",
                                "Programming Language :: Python",
                                "Development Status :: 4 - Beta",
                                "Intended Audience :: Developers",
                                "Intended Audience :: Science/Research",
                                'Intended Audience :: End Users/Desktop',
                                "Topic :: Scientific/Engineering :: GIS"],
                   )

pipy.generate_docs(packpath)
#pipy.upload_test(packpath)
pipy.upload(packpath)

