import os
import io
import unittest

from app import app

image_string = None

class ImageTest(unittest.TestCase):


    # setup and teardown

    # executed prior to each test
    def setUp(self):
        self.dir = os.path.dirname(os.path.realpath(__file__))
        self.app = app.test_client()


    # executed after each test
    def tearDown(self):
        pass


    # Test

    def test_image(self):

        with open(self.dir + '/test_image/scarjo.jpeg', 'rb') as test_image:
            test_imae_BytesIO = io.BytesIO(test_image.read())
            global image_string
            image_string = (test_imae_BytesIO.read())

            test_imae_BytesIO.seek(0)

            response = self.app.post('/',
                                 content_type='multipart/form-data',
                                 data={'file': (test_imae_BytesIO, 'scarjo.jpeg')},
                                 follow_redirects=True)

        assert response.data == image_string;


if __name__ == "__main__":
    unittest.main()