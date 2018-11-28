import os
import asyncio
from time import time
from datetime import datetime

from src.camera import capture_image
from src.temperature_reader import TemperatureReader, DisplayOffError, ImageProcessingError
from src.utils import clear_terminal, print_spinning_cursor
from src.display import DisplayState
from config import config


class TemperatureMonitor:
    def __init__(self, session=None, debug=False):
        self._temperature_reader = TemperatureReader(debug=debug)
        self._session = session
        self._debug_mode = debug
        self._current_temperature = 0
        self._display_state = DisplayState.OFF
        self._invalid_readings = 0
        self._cycle_start_time = None
        self._capture_start_time = None
        self._capture_start_date = None

    async def run(self, cycle_interval=20):
        self._capture_start_time = time()
        self._capture_start_date = datetime.now()
        print("Starting to monitor temperature from display...")
        print("Start time:")
        print(datetime.now())

        while True:
            self._setup_cycle()
            self._capture_and_analyse_image()
            await self._complete_cycle(requested_interval=cycle_interval)

    @property
    def temperature(self) -> int:
        return self._current_temperature

    @temperature.setter
    def temperature(self, new_value: int):
        # If temperature was read correctly it means that display is on
        self.display_state = DisplayState.ON

        if new_value == self.temperature:
            # Do nothing if there is no value change
            return

        self._current_temperature = new_value

        if self._session is not None:
            self._session.publish(config["crossbar"]["topics"]["temperature"], new_value)
            print(f"Send new temperature on topic: {config['crossbar']['topics']['temperature']}")

    @property
    def display_state(self) -> str:
        return self._display_state.name

    @display_state.setter
    def display_state(self, new_state: DisplayState):
        if new_state == self._display_state:
            # Do nothing if there is no state change
            return

        self._display_state = new_state

        if self._session is not None:
            # This check is done to allow Monitor to work also without crossbar connected
            self._session.publish(config['crossbar']['topics']['display'], self.display_state)
            print(f"Send new display state on topic: {config['crossbar']['topics']['display']}")

    def _setup_cycle(self):
        clear_terminal()
        if self._session is not None:
            print("Connected to Crossbar")

        self._show_stats()
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
            self.display_state = DisplayState.OFF
        finally:
            os.remove(image)

    async def _complete_cycle(self, requested_interval):
        cycle_elapsed_time = time() - self._cycle_start_time
        print(f"Cycle completed. Elapsed time: {cycle_elapsed_time} [sec]")

        if cycle_elapsed_time < requested_interval:
            to_sleep = requested_interval - cycle_elapsed_time
            print(f"Waiting {to_sleep} [sec] to complete cycle interval...")
            await asyncio.sleep(to_sleep)

    def _show_stats(self):
        print(f"Last measured temperature: {self.temperature}")
        print(f"Display state: {self.display_state}")
        print(f"Monitor process started on {self._capture_start_date}")
        print(f"Debug mode: {self._debug_mode}")
        print(f"Invalid readings: {self._invalid_readings}")
