import tensorflow as tf

def normalize_img(image, label):
    """Normalizes images: `uint8` -> `float32`."""
    return tf.cast(image, tf.float32) / 255.0, label

def evaluate_model(model_path='/data/mnist_model_improved.keras'):
    mnist = tf.keras.datasets.mnist
    (_, _), (x_test, y_test) = mnist.load_data()

    # Create a test dataset
    ds_test = tf.data.Dataset.from_tensor_slices((x_test, y_test))
    ds_test = ds_test.map(normalize_img).batch(32).cache().prefetch(tf.data.AUTOTUNE)

    model = tf.keras.models.load_model(model_path)
    loss, accuracy = model.evaluate(ds_test, verbose=0)
    print(f"Test Loss: {loss}, Test Accuracy: {accuracy}")

if __name__ == '__main__':
    evaluate_model()
