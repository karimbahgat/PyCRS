import pypi
 
packpath = "pycrs"
pypi.define_upload(packpath,
                   author="Karim Bahgat",
                   author_email="karim.bahgat.norway@gmail.com",
                   license="MIT",
                   name="PyCRS",
                   changes=["First official release"],
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

pypi.generate_docs(packpath)
#pypi.upload_test(packpath)
#pypi.upload(packpath)

