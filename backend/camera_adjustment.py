import os
from time import sleep
from fractions import Fraction
from datetime import datetime

from picamera import PiCamera


def low_light_capture(resolution, folder):
    resolution_as_str = "_".join(map(str, resolution))
    print(f"Capturing low light image for resolution: {resolution_as_str}")
    image_file = os.path.join(folder, f"{resolution_as_str}_low_light.jpg")

    with PiCamera(
            resolution=resolution,
            framerate=Fraction(1, 6),
            sensor_mode=3
    ) as camera:
        camera.shutter_speed = 6000000
        camera.iso = 800
        # Give the camera a good long time to set gains and
        # measure AWB (you may wish to use fixed AWB instead)
        sleep(30)
        camera.exposure_mode = 'off'
        # Finally, capture an image with a 6s exposure. Due
        # to mode switching on the still port, this will take
        # longer than 6 seconds
        camera.capture(image_file)


def normal_capture(resolution, folder):
    resolution_as_str = "_".join(map(str, resolution))
    print(f"Capturing normal image for resolution: {resolution_as_str}")
    image_file = os.path.join(folder, f"{resolution_as_str}_normal.jpg")
    with PiCamera(resolution=resolution) as camera:
        camera.start_preview()
        # Sleep to give camera sensors time to set its light levels
        sleep(5)
        camera.capture(image_file)
        camera.stop_preview()


def sequential_capture(resolution, folder):
    resolution_as_str = "_".join(map(str, resolution))
    print(f"Capturing image sequence for resolution: {resolution_as_str}")
    image_files = [os.path.join(folder, f"{resolution_as_str}_sequence_{i}.jpg") for i in range(3)]

    with PiCamera(
        resolution=resolution,
        framerate=30
    ) as camera:
        # Set ISO to the desired value
        camera.iso = 700
        # Wait for the automatic gain control to settle
        sleep(2)
        # Now fix the values
        camera.shutter_speed = camera.exposure_speed
        camera.exposure_mode = 'off'
        g = camera.awb_gains
        camera.awb_mode = 'off'
        camera.awb_gains = g
        # Finally, take several photos with the fixed settings
        camera.capture_sequence(image_files)


def capture_using_different_modes(cycles=5):
    script_path = os.path.dirname(os.path.abspath(__file__))
    base_folder = os.path.join(script_path, "src", "images", "camera_adjustment")

    resolutions = [
        (1024, 768),
        (1280, 720),
        (3280, 2464)
    ]

    print("Starting to capture images using different camera modes")

    for cycle in range(cycles):
        print(f'Starting cycle #{cycle}')
        current_folder_name = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        destination_folder = os.path.join(base_folder, current_folder_name)
        os.mkdir(destination_folder)

        for resolution in resolutions:
            low_light_capture(resolution, destination_folder)
            normal_capture(resolution, destination_folder)
            sequential_capture(resolution, destination_folder)

        print(f"Cycle {cycle} completed")

    print("Done")


if __name__ == '__main__':
    capture_using_different_modes(cycles=3)
