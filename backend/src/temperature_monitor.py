import os
import asyncio
from time import time
from datetime import datetime
from collections import deque

from src.camera import capture_image
from src.temperature_reader import TemperatureReader, DisplayOffError, ImageProcessingError
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
        self.last_readings = deque()
        self._cycle_start_time = None

    async def run(self, cycle_interval=20):
        print(f"Monitor process started on {datetime.now()}")
        print(f"Requested pooling interval: {cycle_interval} [sec]")
        print(f"Debug mode: {self._debug_mode}")

        while True:
            self._setup_cycle()
            await self._capture_and_analyse_image()
            await self._complete_cycle(requested_interval=cycle_interval)

    @property
    def temperature(self) -> int:
        return self._current_temperature

    @temperature.setter
    def temperature(self, new_value: int):
        # If temperature was read correctly it means that display is on
        # noinspection PyAttributeOutsideInit
        self.display_state = DisplayState.ON

        if new_value == self.temperature:
            # Do nothing if there is no value change
            return

        self._current_temperature = new_value

        self._update_last_readings()
        print(f"Temperature: {new_value}")

        if self._session is not None:
            self._session.publish(config["crossbar"]["topics"]["temperature"], new_value)

    @property
    def display_state(self) -> str:
        return self._display_state.name

    @display_state.setter
    def display_state(self, new_state: DisplayState):
        if new_state == self._display_state:
            # Do nothing if there is no state change
            return

        self._display_state = new_state
        print(f"Display: {self.display_state}")

        if self._session is not None:
            # This check is done to allow Monitor to work also without crossbar connected
            self._session.publish(config['crossbar']['topics']['display'], self.display_state)

    def _update_last_readings(self):
        new_reading = {
            "timestamp": datetime.now().timestamp(),
            "temperature": self.temperature
        }

        if len(self.last_readings) > 50:
            # Keep only only 50 last temperature readings
            self.last_readings.popleft()

        self.last_readings.append(new_reading)

    def _setup_cycle(self):
        self._cycle_start_time = time()

    async def _capture_and_analyse_image(self):
        image = await capture_image()

        try:
            self.temperature = self._temperature_reader.get_temperature(image)
        except ImageProcessingError:
            print("WARNING: Could not convert current image to samples.")
            self._invalid_readings += 1
        except ValueError:
            # Sometimes PIL throws strange error about issue with processing current image
            # Easiest workaround is to reboot system. This situation occurs every ~10 days,
            # so reboot is acceptable solution.
            print("PIL error encountered - rebooting system...")
            os.system("sudo reboot")
        except DisplayOffError:
            self.display_state = DisplayState.OFF
        finally:
            os.remove(image)

    async def _complete_cycle(self, requested_interval):
        cycle_elapsed_time = time() - self._cycle_start_time

        if cycle_elapsed_time < requested_interval:
            to_sleep = requested_interval - cycle_elapsed_time
            await asyncio.sleep(to_sleep)
