import os
from time import sleep
from picamera import PiCamera

script_path = os.path.dirname(os.path.abspath(__file__))
destination_folder = os.path.join(script_path, "camera_testing_images")
print("Capturing image...")

with PiCamera() as camera:
    camera.resolution = (1024, 768)
    camera.rotation = 90

    file_name = f"Rotation_90"
    image_file = os.path.join(destination_folder, file_name)

    sleep(3)
    camera.capture(image_file)

print("Done")
