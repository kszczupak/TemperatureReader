import os
from time import time
from datetime import datetime

from src.camera import capture_image
from src.temperature_reader import TemperatureReader, DisplayOffError, ImageProcessingError
from src.utils import clear_terminal, print_spinning_cursor
from config import config


class TemperatureMonitor:
    def __init__(self, session=None):
        self._temperature_reader = TemperatureReader()
        self._session = session
        self._current_temperature = 0
        self._invalid_readings = 0
        self._cycle_start_time = None
        self._capture_start_time = None
        self._capture_start_date = None

    def run(self, cycle_interval=20):
        self._capture_start_time = time()
        self._capture_start_date = datetime.now()
        print("Starting to monitor temperature from display...")
        print("Start time:")
        print(datetime.now())

        while True:
            self._setup_cycle()
            self._capture_and_analyse_image()
            self._complete_cycle(requested_interval=cycle_interval)

    @property
    def temperature(self):
        return self._current_temperature

    @temperature.setter
    def temperature(self, new_value):
        # Validacja, wyslanie w wamp eventu
        self._current_temperature = new_value

        if self._session is not None:
            self._session.publish(config["crossbar"]["temperature_topic"], new_value)
            print(f"Send new temperature on topic: {config['crossbar']['temperature_topic']}")

    def _setup_cycle(self):
        clear_terminal()
        if self._session is not None:
            print("Connected to Crossbar")

        print(f"Last measured temperature: {self.temperature}")
        print(f"Monitor process started on {self._capture_start_date}")
        self._cycle_start_time = time()
        print(f"Updating temperature...")

    def _capture_and_analyse_image(self):
        image = capture_image()

        try:
            self.temperature = self._temperature_reader.get_temperature(image)
        except ImageProcessingError:
            print("WARNING: Could not convert current image to samples.")
            self._invalid_readings += 1
        except DisplayOffError:
            print("Temperature display is off. Temperature will not be updated in this cycle.")
        finally:
            os.remove(image)

    def _complete_cycle(self, requested_interval):
        cycle_elapsed_time = time() - self._cycle_start_time
        print(f"Cycle completed. Elapsed time: {cycle_elapsed_time} [sec]")
        self._show_stats()

        if cycle_elapsed_time < requested_interval:
            to_sleep = requested_interval - cycle_elapsed_time
            print(f"Waiting {to_sleep} [sec] to complete cycle interval...")
            print_spinning_cursor(to_sleep)

    def _show_stats(self):
        print(f"Invalid readings: {self._invalid_readings}")
