import os

project_root = os.path.dirname(os.path.abspath(__file__))

config = {
    "classifier": os.path.join(project_root, 'classifier', 'classifier.model'),
    "test_images": os.path.join(project_root, 'tests', 'images')
}
