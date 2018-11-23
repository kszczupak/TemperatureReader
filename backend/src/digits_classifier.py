import pickle

from skimage import util

from config import config


class DigitsClassifier:
    def __init__(self):
        self._classifier = None
        self._load_classifier()

    def get_digit_value(self, digit_image):
        digit_image = util.img_as_float(digit_image)
        reshaped_image = digit_image.reshape(1, -1)

        return int(self._classifier.predict(reshaped_image))

    def _load_classifier(self):
        with open(config["classifier"], mode="rb") as file:
            self._classifier = pickle.load(file)
