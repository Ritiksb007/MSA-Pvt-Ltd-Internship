import pandas as pd
import pickle
from datetime import datetime
from flask import Flask, request, jsonify

# Load the trained model
with open('best_model.pkl', 'rb') as f:
    best_model = pickle.load(f)

# Load the original data columns
original_columns = [
    'region', 'manufacturer', 'model', 'condition', 'cylinders', 'fuel', 
    'odometer', 'title_status', 'transmission', 'drive', 'size', 'type', 
    'paint_color', 'lat', 'long', 'car_age'
]

# Define the Flask app
app = Flask(__name__)

# Define a route for the default URL, which loads the form
@app.route('/')
def form():
    return '''
        <html>
            <body>
                <h1>Car Price Prediction</h1>
                <form action="/predict" method="post">
                    <label for="region">Region:</label>
                    <input type="text" id="region" name="region"><br><br>
                    <label for="manufacturer">Manufacturer:</label>
                    <input type="text" id="manufacturer" name="manufacturer"><br><br>
                    <label for="model">Model:</label>
                    <input type="text" id="model" name="model"><br><br>
                    <label for="odometer">Odometer:</label>
                    <input type="number" id="odometer" name="odometer"><br><br>
                    <label for="year">Year:</label>
                    <input type="number" id="year" name="year"><br><br>
                    <label for="fuel">Fuel:</label>
                    <input type="text" id="fuel" name="fuel"><br><br>
                    <input type="submit" value="Predict Price">
                </form>
            </body>
        </html>
    '''

# Define a route to handle the prediction
@app.route('/predict', methods=['POST'])
def predict():
    data = request.form.to_dict()
    df = pd.DataFrame([data])
    
    # Extract the year and calculate car age
    current_year = datetime.now().year
    df['car_age'] = current_year - pd.to_numeric(df['year'])
    
    # Drop the year column
    df = df.drop(columns=['year'])
    
    # Convert data types
    df['odometer'] = pd.to_numeric(df['odometer'])
    
    # Handle missing columns and encode categorical variables
    df = pd.get_dummies(df)
    df = df.reindex(columns=original_columns, fill_value=0)
    
    prediction = best_model.predict(df)
    
    return jsonify({'predicted_price': prediction[0]})

if __name__ == '__main__':
    app.run(debug=True)
