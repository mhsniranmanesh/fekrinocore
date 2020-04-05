import random
import string

from imagekit.processors import ResizeToFill
from imagekit.specs import ImageSpec


class ProfilePictureImage(ImageSpec):
    processors = [ResizeToFill(900, 900)]
    format = 'JPEG'
    options = {'quality': 100}


class ProfilePictureThumbnail(ImageSpec):
    processors = [ResizeToFill(100, 100)]
    format = 'JPEG'
    options = {'quality': 80}


def generate_resized_picture(picture, mode):
    try:
        if mode == 'image':
            image_generator = ProfilePictureImage(source=picture)
        elif mode == 'thumbnail':
            image_generator = ProfilePictureThumbnail(source=picture)
        result = image_generator.generate()
        dest = open(picture.path, mode='bw')
        dest.write(result.read())
        dest.close()
        return True
    except Exception as e:
        #Handle Exception
        return False


def random_string_generator(size=10, chars=string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
