import json

from autobahn.asyncio.component import Component, run

from config import config
from src.temperature_monitor import TemperatureMonitor


class MonitorComponent:
    @classmethod
    def run(cls):
        print(f"Starting {cls.__name__}...")

        run([component])


component = Component(
    transports=f"ws://{config['crossbar']['host']}:{config['crossbar']['port']}/ws",
    realm=config["crossbar"]["realm"]
)


@component.on_join
async def join(session, details):
    print("Successfully connected to Crossbar router")

    temperature_monitor = TemperatureMonitor(
        session=session,
        debug=False  # Do not save bad readings
    )

    def get_current_status():
        response = {
            "temperature": temperature_monitor.temperature,
            "display": temperature_monitor.display_state
        }

        return json.dumps(response)

    def get_last_temperature_readings():
        response = list(temperature_monitor.last_readings)

        return json.dumps(response)

    session.register(
        get_current_status,
        config["crossbar"]["endpoints"]["current_state"]
    )

    session.register(
        get_last_temperature_readings,
        config["crossbar"]["endpoints"]["last_readings"]
    )

    await temperature_monitor.run(
        cycle_interval=10
    )
