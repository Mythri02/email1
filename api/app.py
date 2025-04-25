from flask import Flask, request, jsonify
from transformers import pipeline
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests from your extension

# Load a basic pretrained model
model = pipeline("text-classification", model="distilbert-base-uncased-finetuned-sst-2-english")

# Route for root URL
@app.route('/')
def home():
    return "Welcome to the Phishing Email Detection App!"

# Route for text classification
@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    text = data.get('text', '')

    if not text:
        return jsonify({'error': 'No text provided'}), 400

    result = model(text)[0]
    label = result['label'].lower()

    prediction = 'phishing' if label == 'negative' else 'safe'

    return jsonify({'prediction': prediction})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
