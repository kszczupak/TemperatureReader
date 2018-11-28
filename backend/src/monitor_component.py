import json

from autobahn.asyncio.wamp import ApplicationSession, ApplicationRunner
from autobahn.wamp import auth

from config import config
from src.temperature_monitor import TemperatureMonitor


class MonitorComponent:
    @classmethod
    def run(cls):
        print(f"Starting {cls.__name__}...")

        url = f"ws://{config['crossbar']['host']}:{config['crossbar']['port']}/ws"

        runner = ApplicationRunner(url=url, realm=config["crossbar"]["realm"])
        runner.run(MonitorWAMPComponent)


class MonitorWAMPComponent(ApplicationSession):
    def __init__(self, c=None):
        super().__init__(c)
        self._temperature_monitor = TemperatureMonitor(
            session=self,
            debug=False     # Do not save bad readings
        )

    # TODO add authentication (here and in router configuration)
    def onConnect(self):
        print("Connected to Crossbar!")

        # Temporary connect without authentication
        self.join(config["crossbar"]["realm"])
        # self.join(config["crossbar"]["realm"], ["wampcra"], config["crossbar"]["auth"]["username"])

    def onDisconnect(self):
        print("Disconnected from Crossbar!")

    # def onChallenge(self, challenge):
    #     secret = config["crossbar"]["auth"]["password"]
    #     signature = auth.compute_wcs(secret.encode('utf8'), challenge.extra['challenge'].encode('utf8'))
    #
    #     return signature.decode('ascii')

    async def onJoin(self, details):
        print("Successfully connected to Crossbar router")

        def get_current_status():
            print("Executing procedure...")
            response = {
                "temperature": self._temperature_monitor.temperature,
                "display": self._temperature_monitor.display_state
            }

            return json.dumps(response)

        self.register(
            get_current_status,
            config["crossbar"]["endpoints"]["current_state"]
        )

        await self._temperature_monitor.run(
            cycle_interval=10
        )
