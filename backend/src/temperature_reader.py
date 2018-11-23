import os
from datetime import datetime

from skimage import io, transform, color, filters, morphology, measure, exposure, util
import numpy as np

from config import project_root


class TemperatureReaderError(Exception):
    pass


class DisplayOffError(TemperatureReaderError):
    pass


class ImageProcessingError(TemperatureReaderError):
    pass


class TemperatureReader:
    """
    Class reads temperature value from given image (photo).
    Uses some image processing to extract temperature from image,
    and simple machine learning classifier to read temperature value.
    """

    def __init__(self):
        self.original_image = None
        self.processed_image = None
        self.temperature_digits = tuple()
        self._partially_processed_images = dict()

    def load_and_process_image(self, image_path):
        self.original_image = io.imread(image_path)
        self._detect_display_off()
        self._apply_image_processing()
        self._fetch_temperature_digits()

    def get_temperature(self):
        pass

    def save_digits_to_file(self):
        relative_folder = os.path.join('images', 'digits')
        digits_file_prefix = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

        file_name = f"{digits_file_prefix}_1.jpg"
        self._save_image(self.temperature_digits[0], os.path.join(relative_folder, file_name))

        file_name = f"{digits_file_prefix}_2.jpg"
        self._save_image(self.temperature_digits[1], os.path.join(relative_folder, file_name))

    def _fetch_temperature_digits(self):
        labeled_image = measure.label(self.processed_image)
        image_regions = measure.regionprops(labeled_image)

        if len(image_regions) == 2:
            # Processing returned valid results
            self.temperature_digits = self._determine_digits_order(image_regions)
            return

        # Only one region could be isolated, meaning probably that image processing pipeline could not split
        # temperature to single digits, or there is more regions isolated than expected.
        # In any case this probably means that processing pipeline should be adjusted so save source and
        # fetched temperature images to file
        self._handle_image_processing_error()

    def _detect_display_off(self):
        if exposure.is_low_contrast(self.original_image):
            raise DisplayOffError()

    def _handle_image_processing_error(self):
        """
        Handles case when image processing pipeline could not return valid results.
        All images from image processing pipeline are saved to file.
        """

        bad_images_folder_name = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        bad_images_folder_relative_path = os.path.join('images', 'bad', bad_images_folder_name)

        bad_images_folder_full_path = os.path.join(project_root, bad_images_folder_relative_path)
        os.mkdir(bad_images_folder_full_path)

        for image_name in self._partially_processed_images:
            file = os.path.join(bad_images_folder_relative_path, f"{image_name}.jpg")
            self._save_image(self._partially_processed_images[image_name], file)

        raise ImageProcessingError(f"Was not able to fetch single digits from image. Images was saved"
                                   f" in '{bad_images_folder_relative_path}' folder")

    def _determine_digits_order(self, regions):
        """
        Returns tuple of digits images in correct order
        """
        first_object_position_x = regions[0].centroid[1]
        second_object_position_x = regions[1].centroid[1]

        if first_object_position_x < second_object_position_x:
            return (
                self._pad_and_resize(regions[0].image),
                self._pad_and_resize(regions[1].image)
            )

        return (
            self._pad_and_resize(regions[1].image),
            self._pad_and_resize(regions[0].image)
        )

    def _apply_image_processing(self):
        image_grey = color.rgb2grey(self.original_image)  # Convert to gray scale

        # Invert to get black background and white object
        # Some algorithms do not work correctly in different conditions
        image_grey = util.invert(image_grey)

        threshold_image = self.apply_threshold(image_grey)
        thinned = self.apply_thin(threshold_image)
        clean_image = self.cleanup_image(thinned)

        self._partially_processed_images = {
            "0_original": self.original_image,
            "1_grayed_inverted": image_grey,
            "2_after_threshold": threshold_image,
            "3_thinned": thinned,
            "4_processed": clean_image
        }

        self.processed_image = clean_image

    @staticmethod
    def apply_threshold(image_grey):
        threshold_value = filters.threshold_local(image_grey, block_size=113)
        threshold_image = image_grey > threshold_value

        return threshold_image

    @staticmethod
    def apply_thin(image_grey):
        return morphology.thin(image_grey, max_iter=3)

    @staticmethod
    def cleanup_image(image):
        opened_image = morphology.opening(image, selem=morphology.disk(2))

        return morphology.remove_small_objects(opened_image, min_size=1000)

    @staticmethod
    def _save_image(image, relative_path):
        full_path = os.path.join(project_root, relative_path)
        io.imsave(full_path, image)

    @staticmethod
    def _pad_and_resize(image):
        padded_image = np.pad(image, pad_width=1, mode='constant', constant_values=False)

        # It is important to save width/height ratio when resizing
        # In this case this ratio ~1.4
        return transform.resize(padded_image, (22, 16), mode='reflect', preserve_range=True)


if __name__ == '__main__':
    reader = TemperatureReader()
    reader.load_and_process_image("image_1.jpg")
    reader.save_digits_to_file()
