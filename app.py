from flask import Flask, request, render_template_string, jsonify
from transformers import pipeline
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
CORS(app)

# Load the model once
model = pipeline("text-classification", model="distilbert-base-uncased-finetuned-sst-2-english")

# Home page
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        url = request.form['url']
        try:
            # Fetch URL content
            page = requests.get(url, timeout=5)
            soup = BeautifulSoup(page.content, "html.parser")
            page_text = soup.get_text(separator=' ', strip=True)
            # Predict
            result = predict_email(page_text)
        except Exception as e:
            result = f"Error fetching URL: {str(e)} 🚫"
        return render_template_string(html, result=result)
    return render_template_string(html)

# Predict function
def predict_email(text):
    if not text.strip():
        return "No content found ❓"
    result = model(text)[0]
    label = result['label'].lower()
    if label == 'negative':
        return "Phishing Website 🚨"
    else:
        return "Safe Website ✅"

# API (optional)
@app.route('/predict', methods=['POST'])
def api_predict():
    data = request.get_json()
    url = data.get('url', '')
    if not url:
        return jsonify({'error': 'No URL provided'}), 400
    try:
        page = requests.get(url, timeout=5)
        soup = BeautifulSoup(page.content, "html.parser")
        page_text = soup.get_text(separator=' ', strip=True)
        result = model(page_text)[0]
        label = result['label'].lower()
        prediction = 'phishing' if label == 'negative' else 'safe'
        return jsonify({'prediction': prediction})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# HTML Template
html = """
<!DOCTYPE html>
<html>
<head>
    <title>Phishing URL Detection</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f0f2f5;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: flex-start;
            min-height: 100vh;
            padding-top: 50px;
        }
        h1 {
            color: #333;
        }
        form {
            background: #fff;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            width: 400px;
        }
        input[type="text"] {
            width: 100%;
            padding: 10px;
            margin-top: 10px;
            margin-bottom: 20px;
            border: 1px solid #ccc;
            border-radius: 5px;
            font-size: 16px;
        }
        input[type="submit"] {
            background-color: #4CAF50;
            color: white;
            padding: 12px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            width: 100%;
            font-size: 16px;
        }
        input[type="submit"]:hover {
            background-color: #45a049;
        }
        .result {
            margin-top: 20px;
            font-size: 22px;
            font-weight: bold;
            color: #555;
        }
    </style>
</head>
<body>
    <h1>Phishing URL Detection</h1>
    <form method="post">
        <label for="url">Enter Website URL:</label><br>
        <input type="text" name="url" placeholder="Paste the URL here..."><br>
        <input type="submit" value="Detect">
    </form>
    {% if result %}
        <div class="result">
            {{ result }}
        </div>
    {% endif %}
</body>
</html>
"""

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
