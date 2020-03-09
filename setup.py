try: from setuptools import setup
except: from distutils.core import setup

setup(	long_description=open("README.md").read(), 
	long_description_content_type="text/markdown",
	name="""PyCRS""",
	license="""MIT""",
	author="""Karim Bahgat""",
	author_email="""karim.bahgat.norway@gmail.com""",
	url="""http://github.com/karimbahgat/PyCRS""",
	version="""1.0.2""",
	keywords="""GIS spatial CRS projection coordinate system format""",
	packages=['pycrs', 'pycrs/elements'],
	classifiers=['License :: OSI Approved', 'Programming Language :: Python', 'Development Status :: 5 - Production/Stable', 'Intended Audience :: Developers', 'Intended Audience :: Science/Research', 'Intended Audience :: End Users/Desktop', 'Topic :: Scientific/Engineering :: GIS'],
	description="""GIS package for reading, writing, and converting between CRS formats.""",
	)
