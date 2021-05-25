from urllib.request import urlopen, Request
from typing import NoReturn
from bot_constants import HEADERS

import os
import cv2
import imgaug as ia
import numpy as np
from imgaug import augmenters as iaa

FOLDER = 'imgs/'


def delete_images() -> NoReturn:
    from glob import glob
    from os import path, remove
    files = glob(path.join(FOLDER, '*'))
    for file in files:
        remove(file)
    os.rmdir(FOLDER)


def write(image) -> NoReturn:
    os.mkdir(FOLDER) if not os.path.exists(FOLDER) else False
    cv2.imwrite(FOLDER + '/fim.jpg',
                image[0], [int(cv2.IMWRITE_JPEG_QUALITY), 200])


class Distort:
    def __init__(self, image_url: str):
        self.image = image_url
        self.decoded_image = self.read()

    def read(self) -> np.ndarray:
        req = Request(self.image, data=None, headers=HEADERS)
        img = np.asarray(bytearray(urlopen(req).read()), dtype='uint8')
        return cv2.imdecode(img, cv2.IMREAD_COLOR)

    def augment_images(self) -> NoReturn:
        images = [self.decoded_image]
        ia.seed(np.random.randint(100000, size=1)[0])
        for image in images:
            # image might not have 3 dimensions
            if np.ndim(image) < 3:
                image = image[np.newaxis, :, :]
        # Example batch of images.
        # The array has shape (32, 64, 64, 3) and dtype uint8.

        seq = iaa.Sequential([
            # iaa.Fliplr(0.5), # horizontal flips
            iaa.Crop(percent=(0, 0.5)),  # random crops
            # Small gaussian blur with random sigma between 0 and 0.5.
            # But we only blur about 50% of all images.
            iaa.Sometimes(0.5, iaa.GaussianBlur(sigma=(0, 0.5))),
            # Strengthen or weaken the contrast in each image.
            # iaa.ContrastNormalization((0.75, 1.5)),
            iaa.contrast.LinearContrast((0.75, 1.5)),
            # Add gaussian noise.
            # For 50% of all images, we sample the noise once per pixel.
            # For the other 50% of all images, we sample the noise per pixel AND
            # channel. This can change the color (not only brightness) of the
            # pixels.
            iaa.AdditiveGaussianNoise(loc=0, scale=(0.0, 0.05 * 255), per_channel=0.5),
            # Make some images brighter and some darker.
            # In 20% of all cases, we sample the multiplier once per channel,
            # which can end up changing the color of the images.
            iaa.Multiply((0.8, 1.2), per_channel=0.2),
            # Apply affine transformations to each image.
            # Scale/zoom them, translate/move them, rotate them and shear them.
            iaa.Affine(
                scale={"x": (0.8, 1.2), "y": (0.8, 1.2)},
                translate_percent={"x": (-0.2, 0.2), "y": (-0.2, 0.2)},
                rotate=(-25, 25),
                shear=(-8, 8)
            )
        ], random_order=True)  # apply augmenters in random order

        write(seq.augment_images(images))


if __name__ == '__main__':
    pass
