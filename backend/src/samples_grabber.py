from picamera import PiCamera
import os
from time import sleep, time, strftime, gmtime
from datetime import datetime

from src.image_to_temperature import TemperatureReader


cycle_interval = 120    # Cycle interval in sec
samples_limit = 10    # number of samples to capture
bad_images_limit = 10

capture_image_path = os.path.join('images', 'captured', 'temp.jpg')
camera = PiCamera()


def capture_samples():
    reader = TemperatureReader()
    capture_start_time = time()
    print("Starting to capture temperature samples...")
    print("Start time:")
    print(datetime.now())

    while True:
        cycle_start_time = time()
        capture_image()
        reader.process_image(capture_image_path)
        reader.save_digits_to_file()
        os.remove(capture_image_path)

        if reader.ok_images_count >= samples_limit:
            capture_elapsed_time = time() - capture_start_time
            formatted_time = strftime("%H [h] : %M [min] : %S [sec]", gmtime(capture_elapsed_time))
            print("Capturing successfully complete. Elapsed time:")
            print(formatted_time)
            reader.show_stats()
            return

        if reader.bad_images_count >= bad_images_limit:
            capture_elapsed_time = time() - capture_start_time
            formatted_time = strftime("%H [h] : %M [min] : %S [sec]", gmtime(capture_elapsed_time))
            print("Reached limit of bad samples. Aborting operation.  Elapsed time:")
            print(formatted_time)
            reader.show_stats()
            return

        cycle_elapsed_time = time() - cycle_start_time
        print(f"Cycle completed. Elapsed time: {cycle_elapsed_time} [sec]")

        if cycle_elapsed_time < cycle_interval:
            to_sleep = cycle_interval - cycle_elapsed_time
            print(f"Waiting {to_sleep} [sec] to complete cycle interval...")
            sleep(to_sleep)


def capture_image():
    camera.start_preview()
    # Sleep to give camera sensors time to set its light levels
    sleep(5)
    camera.capture(capture_image_path)
    camera.stop_preview()
