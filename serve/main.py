import tensorflow as tf
from flask import Flask, request, jsonify
import numpy as np

app = Flask(__name__)

try:
    model = tf.keras.models.load_model('/data/mnist_model_improved.keras')
    print("Model loaded successfully")
except:
    model = None
    print("Model not found. Please train the model first.")

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        image = np.array(data['image'], dtype=np.float32).reshape(1, 28, 28, 1)
        if image.max() > 1:
            image = image / 255.0

        predictions = model.predict(image)
        predicted_digit = np.argmax(predictions[0])
        confidence = float(predictions[0][predicted_digit])

        return jsonify({
            'predicted_digit': int(predicted_digit),
            'confidence': confidence
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'model_loaded': model is not None})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3002)
