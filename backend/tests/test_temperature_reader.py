import unittest
import os

from skimage import io

from config import config
from src.digits_classifier import DigitsClassifier
from src.temperature_reader import TemperatureReader, DisplayOffError


class ClassifierTests(unittest.TestCase):

    def test_digits_recognition(self):
        digits_path = os.path.join(config["test_images"], "digits")
        classifier = DigitsClassifier()

        for file in os.listdir(digits_path):
            digit_file_path = os.path.join(digits_path, file)
            digit_image = io.imread(digit_file_path)
            expected_value = int(file[0])
            measured_value = classifier.get_digit_value(digit_image)

            self.assertEqual(expected_value, measured_value)


class ReaderTests(unittest.TestCase):

    def test_temperature_recognition(self):
        images_path = os.path.join(config["test_images"], "display_on")
        reader = TemperatureReader()

        for file in os.listdir(images_path):
            file_path = os.path.join(images_path, file)
            expected_value = int(file[:2])
            measured_value = reader.get_temperature(file_path)

            self.assertEqual(expected_value, measured_value)

    def test_display_off_detection(self):
        image_path = os.path.join(config["test_images"], "display_off", "off_0.jpg")
        reader = TemperatureReader()

        with self.assertRaises(DisplayOffError):
            reader.get_temperature(image_path)


if __name__ == '__main__':
    unittest.main()
