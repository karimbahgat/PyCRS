import unittest

import pycrs

class TestLoaderMethods(unittest.TestCase):
    def test_from_url(self):
        # before patch crs_obj would be None
        crs_obj = pycrs.loader.from_url('http://spatialreference.org/ref/esri/102630/esriwkt/')
        proj4 = crs_obj.to_proj4()
        # make sure it outputs something
        self.assertGreater(len(proj4), 0)
        # does the output seem to be proj4?
        self.assertEqual(proj4[0], '+')

if __name__ == '__main__':
    unittest.main()
