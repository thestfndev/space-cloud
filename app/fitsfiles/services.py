import logging

import matplotlib.pyplot as plt
from astropy.io import fits
from astropy.io.fits import Header
from auto_stretch.stretch import Stretch
from skimage.transform import resize

logger = logging.getLogger()


class FitsService:
    @staticmethod
    def header_to_dict(header: Header) -> dict:
        """
        Convert Header object to JSON.

        This method requires additional logic, as header_items is a list of tuples,
        which sometimes have duplicated keys, which values need to be concatenated.
        """
        header_items = [kv for kv in header.items()]
        header_dict = {}
        for item in header_items:
            k, v = item
            if k not in header_dict:
                header_dict[k] = v.strip() if isinstance(v, str) else v
            else:
                header_dict[k] += v
        return header_dict

    @staticmethod
    def get_file_header_dict(file) -> dict:
        with fits.open(file, mode="readonly") as fits_file:
            fits_head: Header = fits_file.pop().header
            return FitsService.header_to_dict(fits_head)

    @staticmethod
    def generate_thumbnail(path):
        image_data = fits.getdata(path, ext=0)

        stretched_image = Stretch().stretch(image_data)
        ratio = stretched_image.shape[0] / stretched_image.shape[1]
        size = (300 * ratio, 300)

        thumbnail_filepath = path.with_suffix(".jpg")

        image_resized = resize(stretched_image, size, anti_aliasing=True)
        plt.imsave(thumbnail_filepath, image_resized, cmap="gray")
