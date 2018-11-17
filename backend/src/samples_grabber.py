from picamera import PiCamera
import os
from time import sleep, time, strftime, gmtime
from datetime import datetime

from src.temperature_reader import TemperatureReader
from src.utils import clear_terminal, print_spinning_cursor


class SamplesGrabber:
    def __init__(self):
        self._temperature_reader = TemperatureReader()
        self._base_path = os.path.dirname(os.path.abspath(__file__))  # Absolute path to this script; will be used to
        # resolve relative paths
        self._capture_image_path = os.path.join(self._base_path, 'images', 'captured', 'temp.jpg')
        self._camera = None
        self._setup_camera()
        self._cycle_start_time = None
        self._capture_start_time = None
        self._capture_start_date = None
        self._samples_limit = None
        self._bad_images_limit = None

    def _setup_camera(self):
        self._camera = PiCamera()
        self._camera.resolution = (3280, 2464)  # Use full resolution of camera; in my case this is useful, because
        # camera is placed ~2 meters from display

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

            if self._temperature_reader.ok_images_count >= self._samples_limit:
                print("Capturing successfully complete. Elapsed time:")
                self._display_exit_message()
                return

            if self._temperature_reader.bad_images_count >= self._bad_images_limit:
                print("Reached limit of bad samples. Aborting operation.  Elapsed time:")
                self._display_exit_message()
                return

            if self._temperature_reader.is_display_off():
                print("Temperature display is off. Samples was not gathered in this cycle.")

            self._complete_cycle(requested_interval=cycle_interval)

    def _setup_cycle(self):
        clear_terminal()
        print(f"Capturing process started on {self._capture_start_date}")
        self._cycle_start_time = time()
        print(f"Starting processing cycle...")

    def _capture_and_analyse_image(self):
        self._capture_image()
        self._temperature_reader.process_image(self._capture_image_path)
        self._temperature_reader.save_digits_to_file()
        os.remove(self._capture_image_path)

    def _capture_image(self):
        self._camera.start_preview()
        # Sleep to give camera sensors time to set its light levels
        sleep(5)
        self._camera.capture(self._capture_image_path)
        self._camera.stop_preview()

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
        print(f"Valid samples gathered: {self._temperature_reader.ok_images_count}/{self._samples_limit}")
        print(f"Bad images gathered: {self._temperature_reader.bad_images_count}/{self._bad_images_limit}")
