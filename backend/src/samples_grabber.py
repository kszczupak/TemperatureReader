import os
from time import time, strftime, gmtime
from datetime import datetime

from src.camera import capture_image
from src.temperature_reader import TemperatureReader, DisplayOffError, ImageProcessingError
from src.utils import clear_terminal, print_spinning_cursor


class SamplesGrabber:
    def __init__(self):
        self._temperature_reader = TemperatureReader(debug=True)
        self._ok_samples_collected = 0
        self._bad_samples_collected = 0
        self._cycle_start_time = None
        self._capture_start_time = None
        self._capture_start_date = None
        self._samples_limit = None
        self._bad_images_limit = None

    def fetch_samples(self, cycle_interval=120, samples_limit=1000, bad_images_limit=10):
        self._capture_start_time = time()
        self._capture_start_date = datetime.now()
        self._samples_limit = samples_limit
        self._bad_images_limit = bad_images_limit
        print("Starting to capture temperature samples...")
        print("Start time:")
        print(datetime.now())

        while True:
            self._setup_cycle()
            self._capture_and_analyse_image()

            if self._ok_samples_collected >= self._samples_limit:
                print("Capturing successfully complete. Elapsed time:")
                self._display_exit_message()
                return

            if self._bad_samples_collected >= self._bad_images_limit:
                print("Reached limit of bad samples. Aborting operation.  Elapsed time:")
                self._display_exit_message()
                return

            self._complete_cycle(requested_interval=cycle_interval)

    def _setup_cycle(self):
        clear_terminal()
        print(f"Capturing process started on {self._capture_start_date}")
        self._cycle_start_time = time()
        print(f"Starting processing cycle...")

    def _capture_and_analyse_image(self):
        image = capture_image()

        try:
            self._temperature_reader.load_and_process_image(image)
            self._temperature_reader.save_digits_to_file()
            self._ok_samples_collected += 2
        except ImageProcessingError:
            print("WARNING: Could not convert current image to samples.")
            self._bad_samples_collected += 1
        except DisplayOffError:
            print("Temperature display is off. Samples was not gathered in this cycle.")
        finally:
            os.remove(image)

    def _display_exit_message(self):
        capture_elapsed_time = time() - self._capture_start_time
        formatted_time = strftime("%H[h]:%M[min]:%S[sec]", gmtime(capture_elapsed_time))
        print(formatted_time)
        self._show_stats()

    def _complete_cycle(self, requested_interval):
        cycle_elapsed_time = time() - self._cycle_start_time
        print(f"Cycle completed. Elapsed time: {cycle_elapsed_time} [sec]")
        self._show_stats()

        if cycle_elapsed_time < requested_interval:
            to_sleep = requested_interval - cycle_elapsed_time
            print(f"Waiting {to_sleep} [sec] to complete cycle interval...")
            print_spinning_cursor(to_sleep)

    def _show_stats(self):
        print("Current metrics:")
        print(f"Valid samples gathered: {self._ok_samples_collected}/{self._samples_limit}")
        print(f"Bad images gathered: {self._bad_samples_collected}/{self._bad_images_limit}")
