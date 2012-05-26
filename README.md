peekimagedata
=============

Contains functions to peek image metadata by looking at an image stream's
metadata.

Use like this:

    import peekimagedata

    # 24 bytes of header data always are enough for a png. A jpeg can contain
    # a thumbnail or EXIF data before the frame information, so there's no
    # clear bound for jpegs, but 50kB are often enough.
    png_data = open('kitten.png').read(24)
    try:
      width, height = peekimagedata.peek_dimensions(png_data)
      print width, height
    except ValueError:
      print 'Failed to get image dimensions'
