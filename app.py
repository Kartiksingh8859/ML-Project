from flask import Flask, request, render_template
import numpy as np
import pandas as pd

from sklearn.preprocessing import StandardScaler
from src.pipeline.predict_pipeline import CustomData, PredictPipeline

application = Flask(__name__)  # Entry point
app = application

# Route for the home page
@app.route('/')
def index():
    return render_template('index.html') 

@app.route('/predictdata', methods=['GET', 'POST'])
def predict_datapoint():
    if request.method == 'GET':
        return render_template('home.html')
    else:
        data = CustomData(
            gender=request.form.get('gender'),
            ethnicity=request.form.get('ethnicity'),
            parental_level_of_education=request.form.get('parental_level_of_education'),
            lunch=request.form.get('lunch'),
            test_preparation_course=request.form.get('test_preparation_course'),
            math_score=float(request.form.get('math_score')),
            reading_score=float(request.form.get('reading_score'))
        )
        
        pred_df = data.get_data_as_data_frame()

        print(pred_df)
        print("Before Prediction")

        predict_pipeline = PredictPipeline()
        print("Mid Prediction")

        predicted_writing_score = round((predict_pipeline.predict(pred_df)[0]),2)
        print("After Prediction")
        
        # Calculate the average score
        average_score = round((data.math_score + data.reading_score + predicted_writing_score) / 3, 2)
        
        return render_template('home.html', predicted_writing_score=predicted_writing_score, average_score=average_score)

if name == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)