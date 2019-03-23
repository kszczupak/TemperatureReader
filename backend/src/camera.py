import os
import asyncio

from picamera import PiCamera

from config import project_root


async def capture_image(image_file_name='image.jpg'):
    with PiCamera() as camera:
        image_file = os.path.join(project_root, 'images', 'captured', image_file_name)
        resolution = (3280, 2464)
        camera.resolution = resolution
        camera.rotation = 270
        camera.zoom = (
            0.49,    # start x
            0.463,  # start y
            0.031,  # width
            0.031   # height
        )
        camera.exposure_mode = 'night'
        camera.image_effect = 'negative'

        # Resize captured image 10x
        resize_resolution = tuple(map(lambda x: int(x / 10), resolution))

        await asyncio.sleep(3)
        camera.capture(image_file, resize=resize_resolution)

    return image_file

