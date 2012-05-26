import struct


_JPEG_SOI = '\xff\xd8'
_JPEG_MARKER_EOI = '\xd9'
_JPEG_MARKER_SOF0 = 0xc0
def _peek_dimensions_jpeg(data):
    '''Returns  (width, height) for a jpeg image. Because EXIF data and
    thumbnails can precede the start-of-frame marker, it's unknown how much
    header data this function needs. Raises ValueError on failure.'''
    if data[:2] != _JPEG_SOI:
        raise ValueError('Invalid JPEG data, expected Start Of Image tag')
    idx, n = 2, len(data)

    frame = struct.Struct('>BBH')
    while idx + 1 < n:
        if data[idx] != '\xff':
            raise ValueError('Invalid JPEG data, expected start of chunk')
        if data[idx + 1] == _JPEG_MARKER_EOI:
            raise ValueError(
                'Invalid JPEG data, End Of Image before Start Of Frame')
        ff, marker, size = frame.unpack_from(data, idx)

        # 0xFx are start-of-frame markers, except for
        #   0xc4, DHT (define huffman tables)
        #   0xcc, DAC (define arithmetic coding)
        # libjpeg only implements c0, c1, c2, c9, ca, but they all share the
        # same header.
        if ((marker & 0xF0) == _JPEG_MARKER_SOF0 and
            (marker & 0x0F) not in (0x4, 0xc)):
            height, width = struct.unpack_from('>xHH', data, idx + 4)
            return width, height

        idx += size + 2  # size doesn't include (ff, marker)
    raise ValueError('Invalid JPEG data, no End Of Image')


_PNG_MAGIC = '\x89PNG\r\n\x1a\n'
def _peek_dimensions_png(data):
    '''Returns  (width, height) for a png image. Needs at least 24 bytes of
    header data. Raises ValueError on failure.'''
    if data[:8] != _PNG_MAGIC:
       raise ValueError('Invalid PNG data, expected PNG header')

    if len(data) < 24:
       raise ValueError('Need at least 24 bytes of png data')

    # IHDR must always be the first chunk.
    size, fourcc = struct.unpack_from('>I4s', data, 8)
    if fourcc != 'IHDR':
        raise ValueError('Invalid PNG data, expected IHDR chunk')

    width, height = struct.unpack_from('>II', data, 16)
    return width, height


def peek_dimensions(data):
    '''Returns (width, height) for a png or jpeg image stream. Raises ValueError
    on failure.

    24 bytes of header data always are enough for a png. A jpeg can contain
    a thumbnail or EXIF data before the frame information, so there's no
    clear bound for jpegs, but 50kB are often enough.'''
    if data[:2] == _JPEG_SOI:
       return _peek_dimensions_jpeg(data)
    if data[:8] == _PNG_MAGIC:
       return _peek_dimensions_png(data)
    raise ValueError('Unknown image type')


def peek_mimetype(data):
    '''Returns the mimetype for a png or jpeg image stream. Raises ValueError
    on failure.

    Bases its decision on the first few bytes of data, doesn't check for
    image validity.'''
    if data[:2] == _JPEG_SOI:
       return 'image/jpeg'
    if data[:8] == _PNG_MAGIC:
       return 'image/png'
    raise ValueError('Unknown image type')
