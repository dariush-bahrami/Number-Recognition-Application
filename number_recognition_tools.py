def convert_image_to_mnist_format(image_path: str):
    from PIL import Image
    import numpy as np

    original_image = Image.open(image_path)
    resized_image = original_image.resize((28, 28))
    greyscale_image = resized_image.convert('L')

    image_array = np.asarray(greyscale_image)
    scaled_image_array = image_array / 255
    inverted_image_array = np.ones((28, 28)) - scaled_image_array

    return inverted_image_array


def conv_net_compatible_image(path: str):
    import numpy as np

    mnist_image = convert_image_to_mnist_format(path)
    image = mnist_image.reshape((28, 28, 1))
    return np.array([image])


def predict_number_image(model_path, image_path):
    from tensorflow.keras.models import load_model
    model = load_model(model_path)
    image_array = conv_net_compatible_image(image_path)
    prediction = model.predict_classes(image_array)
    return prediction[0]