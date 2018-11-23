import os

project_root = os.path.dirname(os.path.abspath(__file__))

config = {
    "classifier": os.path.join(project_root, 'classifier', 'classifier.model'),
    "test_images": os.path.join(project_root, 'tests', 'images'),
    "crossbar": {
        "host": "192.168.1.69",
        "port": "8080",
        "realm": "realm1",
        "temperature_topic": "TEMPERATURE_UPDATE"
    }
}
