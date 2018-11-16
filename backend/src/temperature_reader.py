from skimage import io, transform, color, filters, morphology, measure
import numpy as np
from uuid import uuid4
import os

import matplotlib.pyplot as plt


class TemperatureReader:
    """
    Class reads temperature value from given image (photo).
    Uses some image processing to extract temperature from image,
    and simple machine learning classifier to read temperature value.
    """

    def __init__(self):
        self.temperature_image = None
        self.first_digit = None
        self.second_digit = None
        self.bad_images_count = 0
        self.ok_images_count = 0
        self._base_path = os.path.dirname(os.path.abspath(__file__))

    def process_image(self, image_path):
        self.temperature_image = None
        self.first_digit = None
        self.second_digit = None
        self.temperature_image = self.fetch_temperature(image_path)
        self._fetch_temperature_digits()

    def is_display_off(self):
        """
        Checks if display with temperature digits is off.
        Method checks currently processed image, so caller
        is expected to invoke process_image method first in
        order to update current image.
        :return: True is display is off; False otherwise
        """
        # For now check if processing of the current image resulted in isolating valid digits.
        # This can be misleading in some cases, so it can be replaced with more sophisticated method.
        # E.g. some trained context classifier.
        return self.first_digit is None or self.second_digit is None

    def show_temperature_image(self):
        fig, ax = plt.subplots()
        ax.imshow(self.temperature_image)
        ax.set_xticks([])
        ax.set_yticks([])
        plt.show()

    def save_digits_to_file(self):
        if self.is_display_off():
            return

        path = os.path.join('images', 'digits')

        file_name = f"{uuid4()}.jpg"
        self.save_image(self.first_digit, os.path.join(path, file_name))
        self.ok_images_count += 1

        file_name = f"{uuid4()}.jpg"
        self.save_image(self.second_digit, os.path.join(path, file_name))
        self.ok_images_count += 1

    @classmethod
    def fetch_temperature(cls, raw_image_path):
        full_image = cls.load_image(raw_image_path)
        temperature_image_color = cls.fetch_temperature_area(full_image)
        processed_temperature_image = cls.apply_image_processing(temperature_image_color)

        return processed_temperature_image

    @staticmethod
    def load_image(image_path):
        return io.imread(image_path)

    @staticmethod
    def fetch_temperature_area(full_image):
        x1, y1, x2, y2 = 1582, 1220, 1640, 1148
        temperature_area = full_image[y2:y1, x1:x2]
        return transform.rotate(temperature_area, 90, resize=True)

    @classmethod
    def apply_image_processing(cls, image):
        image_grey = cls.convert_to_grey(image)
        threshold_image = cls.apply_threshold(image_grey)
        thinned = cls.apply_thin(threshold_image)
        clean_image = cls.cleanup_image(thinned)

        return clean_image

    @staticmethod
    def convert_to_grey(image_color):
        return color.rgb2grey(image_color)

    @staticmethod
    def apply_threshold(image_grey):
        threshold_value = filters.threshold_local(image_grey, block_size=23)
        threshold_image = image_grey > threshold_value

        return threshold_image

    @staticmethod
    def apply_thin(image_grey):
        return morphology.thin(image_grey, max_iter=3)

    @staticmethod
    def cleanup_image(image):
        opened_image = morphology.opening(image, selem=morphology.disk(2))

        return morphology.remove_small_objects(opened_image, min_size=100)

    def save_image(self, image, relative_path):
        full_path = os.path.join(self._base_path, relative_path)
        io.imsave(full_path, image)

    def _fetch_temperature_digits(self):
        labeled_image = measure.label(self.temperature_image)
        image_regions = measure.regionprops(labeled_image)

        if len(image_regions) == 2:
            # Processing returned valid results
            self.first_digit = self._pad_and_resize(image_regions[0].image)
            self.second_digit = self._pad_and_resize(image_regions[1].image)
            return

        elif len(image_regions) == 0:
            # No region could be isolated
            # Probably screen is off, so do nothing
            return

        # Only one region could be isolated, meaning probably that image processing pipeline could not split
        # temperature to single digits, or there is more regions isolated than expected.
        # In any case this probably means that processing pipeline should be adjusted so save source
        # temperature image to file
        bad_image_name = f"{uuid4()}.jpg"
        print(f"Warning: Was not able to fetch single digits from image. Image was saved as {bad_image_name}")
        path = os.path.join('images', 'bad', bad_image_name)
        self.save_image(self.temperature_image, path)
        self.bad_images_count += 1

    @staticmethod
    def _pad_and_resize(image):
        padded_image = np.pad(image, pad_width=1, mode='constant', constant_values=False)

        return transform.resize(padded_image, (35, 25), mode='reflect', preserve_range=True)


if __name__ == '__main__':
    reader = TemperatureReader()
    reader.process_image("jasne.jpg")
    reader.save_digits_to_file()
