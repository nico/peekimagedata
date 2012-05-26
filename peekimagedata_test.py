import peekimagedata
import unittest


class TestPeekDimensions(unittest.TestCase):
    def assertSize(self, expected_size, image):
        size = peekimagedata.peek_dimensions(open(image).read())
        self.assertEqual(expected_size, size)

    def test_png(self):
        # A regular png.
        self.assertSize((947, 639), 'tests/sergey-stark.png')

    def test_jpeg(self):
        # A regular jpeg.
        self.assertSize((471, 700), 'tests/escher.jpeg')

    def test_jpeg_exif(self):
        # A jpeg with exif data, doesn't have its file size in the first 5kB.
        self.assertSize((545, 370), 'tests/exif-data.jpeg')

    def test_empty_data(self):
        self.assertRaises(ValueError, peekimagedata.peek_dimensions, '')

    def test_empty_jpeg(self):
        self.assertRaises(ValueError,
                          peekimagedata.peek_dimensions, '\xff\xd8\xff\xd9')

    def test_empty_jpeg(self):
        self.assertRaises(ValueError,
                          peekimagedata.peek_dimensions, '\xff\xd8\xff\xd9')

    def test_empty_png(self):
        self.assertRaises(ValueError,
                          peekimagedata.peek_dimensions, '\x89PNG\r\n\x1a\n')


class TestPeekMimetype(unittest.TestCase):
    def assertMimetype(self, expected_mimetype, image):
        mimetype = peekimagedata.peek_mimetype(open(image).read())
        self.assertEqual(expected_mimetype, mimetype)

    def test_png(self):
        self.assertMimetype('image/png', 'tests/sergey-stark.png')

    def test_jpeg(self):
        self.assertMimetype('image/jpeg', 'tests/escher.jpeg')


if __name__ == '__main__':
    unittest.main()
