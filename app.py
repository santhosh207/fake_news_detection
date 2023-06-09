from flask import Flask, request, jsonify, render_template
import pickle
import numpy as np
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Load the SVM model and TfidfVectorizer from the pickle files
with open('model12.pkl', 'rb') as f:
    model = pickle.load(f)

with open('vector.pkl', 'rb') as f:
    vectorizer = pickle.load(f)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Get the text input from the form
    text = request.form.get('text')
    if text is not None:
        # Transform the text using the TfidfVectorizer
        text_transformed = vectorizer.transform([text])

        # Make the prediction using the SVM model
        prediction = model.predict(text_transformed)[0]

        # Return the prediction as a JSON object
        return jsonify({'prediction': int(prediction)})
    else:
        return jsonify({'error': 'Input text not provided.'})

if __name__ == '__main__':
    app.run(debug=True)
