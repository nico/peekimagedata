import peekimagedata
import unittest


class TestPeekimagedata(unittest.TestCase):
    def assertSize(self, image, expected_size):
        size = peekimagedata.peek_dimensions(open(image).read())
        self.assertEqual(expected_size, size)

    def test_png(self):
        # A regular png.
        self.assertSize('tests/sergey-stark.png', (947, 639))

    def test_jpeg(self):
        # A regular jpeg.
        self.assertSize('tests/escher.jpeg', (471, 700))

    def test_jpeg_exif(self):
        # A jpeg with exif data, doesn't have its file size in the first 5kB.
        self.assertSize('tests/exif-data.jpeg', (545, 370))

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


if __name__ == '__main__':
    unittest.main()
