import argparse

from src.temperature_monitor import TemperatureMonitor

parser = argparse.ArgumentParser()
parser.add_argument("-cycle_interval", "-i", type=int, help="Interval between pooling cycles in [sec]", default=20)

args = parser.parse_args()

monitor = TemperatureMonitor()
monitor.run(
    cycle_interval=args.cycle_interval
)
