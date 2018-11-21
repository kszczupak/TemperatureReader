from src.camera import capture_image

print("Capturing images...")

for i in range(5):
    print(f"Capturing image #{i}")
    capture_image(f"image_{i}.jpg")

print("Done")
