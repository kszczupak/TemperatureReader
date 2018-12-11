from autobahn.asyncio.component import Component, run
import asyncio

from config import config


class FakeFrontendComponent:
    @classmethod
    def run(cls):
        print(f"Starting {cls.__name__}...")

        run([component])


component = Component(
    transports=f"ws://{config['crossbar']['host']}:{config['crossbar']['port']}/ws",
    realm=config["crossbar"]["realm"]
)


@component.subscribe(topic=config["crossbar"]["topics"]["temperature"])
def on_temperature_change(new_temperature):
    print(f"Current temperature: {new_temperature}")


@component.on_join
async def join(session, details):
    print("Successfully connected to Crossbar router")

    while True:
        results = await session.call(config["crossbar"]["endpoints"]["current_state"])
        print(results)
        await asyncio.sleep(15)
