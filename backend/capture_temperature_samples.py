from src.samples_grabber import SamplesGrabber

if __name__ == '__main__':
    grabber = SamplesGrabber()
    grabber.fetch_samples(
        cycle_interval=60,
        samples_limit=2000,
        bad_images_limit=20
    )
