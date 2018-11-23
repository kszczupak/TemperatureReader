import os
import pickle

from sklearn import svm, metrics, model_selection
from skimage import io, util

from config import project_root, config


def train_and_save_classifier():
    model = train_model()
    save_model(model)


def train_model():
    training_data, test_data, training_target, test_target = load_training_data()

    model = svm.SVC(gamma=0.001)
    # classifiers = {
    #     "SVM gamma=0.001": svm.SVC(gamma=0.001)
    #     # "SVM gamma=0.01": svm.SVC(gamma=0.01),
    #     # "SVM": svm.SVC(),
    #     # "Logistic Regression": linear_model.LogisticRegression()
    # }

    model.fit(training_data, training_target)

    predicted = model.predict(test_data)
    score = metrics.accuracy_score(test_target, predicted)
    print(f"Score: {score}")
    print(metrics.classification_report(test_target, predicted))

    return model


def load_training_data():
    training_data_folder = os.path.join(project_root, 'images', 'training_data')
    excluded_files = ['.gitignore']
    training_data = list()
    training_target = list()
    print("Loading training data...")

    for target in os.listdir(training_data_folder):
        current_dir = os.path.join(training_data_folder, target)

        for file in os.listdir(current_dir):
            if file in excluded_files:
                continue

            image_file = os.path.join(current_dir, file)
            image = io.imread(image_file)

            # Need to convert features (image pixels) to <0, 1> range
            image = util.img_as_float(image)
            training_data.append(image.flatten())
            training_target.append(int(target))

    print("Done")

    return model_selection.train_test_split(training_data, training_target)


def save_model(model):
    model_path = config["classifier"]
    with open(model_path, mode="wb") as model_file:
        pickle.dump(model, model_file)


if __name__ == '__main__':
    train_and_save_classifier()
    with open(config["classifier"], mode="rb") as clf_file:
        classifier = pickle.load(clf_file)

    test_file = os.path.join(config["test_images"], "digits", "1.jpg")
    test_image = io.imread(test_file)
    test_image = util.img_as_float(test_image)
    value = classifier.predict(test_image.reshape(1, -1))
    print(f"Loaded file: {test_file}")
    print(f"Predicted value: {int(value)}")
