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
        #app.config['TESTING'] = True
        #app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        self.app = app.test_client()


    # executed after each test
    def tearDown(self):
        pass


    # Test

    def test_image(self):

        with open(self.dir + '/test_image/scarjo.jpeg', 'rb') as img1:
            img1StringIO = io.BytesIO(img1.read())
            global image_string
            image_string = (img1StringIO.read())

            img1StringIO.seek(0)

            response = self.app.post('/',
                                 content_type='multipart/form-data',
                                 data={'file': (img1StringIO, 'scarjo.jpeg')},
                                 follow_redirects=True)

        assert response.data == image_string;


if __name__ == "__main__":
    unittest.main()