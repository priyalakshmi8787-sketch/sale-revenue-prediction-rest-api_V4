
# Import necessary libraries
import numpy as np
import joblib  # For loading the serialized model
import pandas as pd  # For data manipulation
from flask import Flask, request, jsonify  # For creating the Flask API, handling http requests

# Initialize Flask app with a name
superkart_api = Flask("Superkart Sale Revenue Predictor") # Define the name of the app

# Load the trained sale revenue prediction model
model = joblib.load("sale_revenue_prediction_model_v1_0.joblib") # Define the location of the serialized model

# Define a route for the home page
@superkart_api.get('/')
def home():
    """
    This function handles GET requests to the root URL ('/') of the API.
    It returns a simple welcome message.
    """
    return "Welcome to the Superkart Sale Revenue Prediction API!" # Define a welcome message

# Define an endpoint to predict sale revenue for a single customer
@superkart_api.post('/v1/salepredict')
def predict_sales():
    # Get JSON data from the request
    data = request.get_json()

    # Extract relevant customer features from the input data. The order of the column names matters.
    sample = {
        'Product_Weight': data['Product_Weight'],
        'Product_Sugar_Content': data['Product_Sugar_Content'],
        'Product_Allocated_Area': data['Product_Allocated_Area'],
        'Product_MRP': data['Product_MRP'],
        'Store_Size': data['Store_Size'],
        'Store_Location_City_Type': data['Store_Location_City_Type'],
        'Store_Type': data['Store_Type'],
        'Product_Id_char': data['Product_Id_char'],
        'Store_Age_Years': data['Store_Age_Years'],
        'Product_Type_Category': data['Product_Type_Category']
    }

    # Convert the extracted data into a DataFrame
    input_data = pd.DataFrame([sample])

    # Make a sale revenue prediction using the trained model
    prediction = model.predict(input_data).tolist()[0]

    # Return the prediction as a JSON response
    return jsonify({'Sales': prediction})

# Define an endpoint for batch prediction (POST request)
@superkart_api.post('/v1/salepredictbatch')
def predict_sales_batch():
    """
    This function handles POST requests to the '/v1/salepredictbatch' endpoint.
    It expects a CSV file containing property details for multiple properties
    and returns the predicted rental prices as a dictionary in the JSON response.
    """
    # Get the uploaded CSV file from the request
    file = request.files['file']

    # Read the CSV file into a Pandas DataFrame
    input_data = pd.read_csv(file)

    # Make predictions for all properties in the DataFrame (get log_prices)
    predictions = model.predict(input_data).tolist()

    return jsonify({
        "Sales": predictions
    })

# Run the Flask app in debug mode
if __name__ == '__main__':
    superkart_api.run(debug=True)
