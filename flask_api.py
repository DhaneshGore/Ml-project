# -*- coding: utf-8 -*-

<<<<<<< HEAD
from flask import Flask, request, jsonify
=======
from flask import Flask, request
>>>>>>> 414bd701120651d6d9ddd31d44e9f58191f926eb
import numpy as np
import pickle
import pandas as pd
from flasgger import Swagger

app = Flask(__name__)
Swagger(app)

pickle_in = open("logreg.pkl", "rb")
model = pickle.load(pickle_in)

@app.route('/predict', methods=["GET"])
def predict_class():
    """Predict if Customer would buy the product or not.
    ---
    parameters:  
      - name: age
        in: query
        type: number
        required: true
      - name: new_user
        in: query
        type: number
        required: true
      - name: total_pages_visited
        in: query
        type: number
        required: true
      
    responses:
        200:
            description: Successful Prediction
            examples:
                prediction: "0" or "1"
        400:
            description: Bad Request
        500:
            description: Internal Server Error
    """
    try:
        age = int(request.args.get("age"))
        new_user = int(request.args.get("new_user"))
        total_pages_visited = int(request.args.get("total_pages_visited"))
        
        prediction = model.predict([[age, new_user, total_pages_visited]])
        return jsonify({"prediction": int(prediction[0])}), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/predict_file', methods=["POST"])
def prediction_test_file():
    """Prediction on multiple input test file.
    ---
    parameters:
      - name: file
        in: formData
        type: file
        required: true
      
    responses:
        200:
            description: Successful Predictions
            examples:
                predictions: [0, 1, 0]
        400:
            description: Bad Request
        500:
            description: Internal Server Error
    """
    try:
        df_test = pd.read_csv(request.files.get("file"))
        
        # Ensure the dataframe has the right shape and columns
        if df_test.shape[1] != 3:
            return jsonify({"error": "Input file must have exactly three columns."}), 400
        
        prediction = model.predict(df_test)
        
        return jsonify({"predictions": list(prediction)}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
