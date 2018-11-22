import argparse

from src.samples_grabber import SamplesGrabber

parser = argparse.ArgumentParser()
parser.add_argument("-cycle_interval", "-i", type=int, help="Interval between pooling cycles in [sec]", default=60)
parser.add_argument("-samples_limit", "-v", type=int, help="Limit of valid samples to gather", default=2000)
parser.add_argument("-bad_samples_limit", "-b", type=int, help="Limit of not processed samples to gather", default=20)

args = parser.parse_args()

grabber = SamplesGrabber()
grabber.fetch_samples(
        cycle_interval=args.cycle_interval,
        samples_limit=args.samples_limit,
        bad_images_limit=args.bad_samples_limit
    )
