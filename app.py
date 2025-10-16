from flask import Flask, request, render_template
import pickle
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
import xgboost

application = Flask(__name__)
app = application

# Load the pre-trained model and scaler
model = pickle.load(open('XBGR_Model_Agriculture_Yield_Prediction.pkl', 'rb'))
scaler = pickle.load(open('Scalar_Model_Agriculture_Yield_Prediction.pkl', 'rb'))

# Define the feature names used during training
feature_names = [
    'Rainfall_mm', 'Temperature_Celsius', 'Fertilizer_Used', 'Irrigation_Used', 'Days_to_Harvest',
    'Region_East', 'Region_North', 'Region_South', 'Region_West',
    'Soil_Type_Chalky', 'Soil_Type_Clay', 'Soil_Type_Loam', 'Soil_Type_Peaty', 'Soil_Type_Sandy', 'Soil_Type_Silt',
    'Crop_Barley', 'Crop_Cotton', 'Crop_Maize', 'Crop_Rice', 'Crop_Soybean', 'Crop_Wheat',
    'Weather_Condition_Cloudy', 'Weather_Condition_Rainy', 'Weather_Condition_Sunny'
]

@app.route('/')
def home():
    return render_template('home.html')  # Home page for initial greeting or instructions

@app.route('/index', methods=['GET'])
def index():
    return render_template('index.html')  # Index page where user inputs data for prediction

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        try:
            # Retrieve form data and validate
            Temperature_Celsius = float(request.form['Temperature_Celsius'])
            if not (-10 <= Temperature_Celsius <= 50):
                raise ValueError("Temperature must be between -10°C and 50°C.")
            
            Rainfall_mm = float(request.form['Rainfall_mm'])
            if not (0 <= Rainfall_mm <= 1500):
                raise ValueError("Rainfall must be between 0 mm and 1500 mm.")
            
            Days_to_Harvest = int(request.form['Days_to_Harvest'])
            if not (1 <= Days_to_Harvest <= 365):
                raise ValueError("Days to Harvest must be between 1 and 365 days.")
            
            Fertilizer_Used = 1 if 'Fertilizer_Used' in request.form else 0
            Irrigation_Used = 1 if 'Irrigation_Used' in request.form else 0
            
            # One-hot encoding for Region
            region = request.form['Region']
            Region_East = 1 if region == 'East' else 0
            Region_North = 1 if region == 'North' else 0
            Region_South = 1 if region == 'South' else 0
            Region_West = 1 if region == 'West' else 0

            # One-hot encoding for Soil Type
            soil_type = request.form['Soil_Type']
            Soil_Type_Chalky = 1 if soil_type == 'Chalky' else 0
            Soil_Type_Clay = 1 if soil_type == 'Clay' else 0
            Soil_Type_Loam = 1 if soil_type == 'Loam' else 0
            Soil_Type_Peaty = 1 if soil_type == 'Peaty' else 0
            Soil_Type_Sandy = 1 if soil_type == 'Sandy' else 0
            Soil_Type_Silt = 1 if soil_type == 'Silt' else 0

            # One-hot encoding for Crop
            crop = request.form['Crop']
            Crop_Barley = 1 if crop == 'Barley' else 0
            Crop_Cotton = 1 if crop == 'Cotton' else 0
            Crop_Maize = 1 if crop == 'Maize' else 0
            Crop_Rice = 1 if crop == 'Rice' else 0
            Crop_Soybean = 1 if crop == 'Soybean' else 0
            Crop_Wheat = 1 if crop == 'Wheat' else 0

            # One-hot encoding for Weather Condition
            weather = request.form['Weather_Condition']
            Weather_Condition_Cloudy = 1 if weather == 'Cloudy' else 0
            Weather_Condition_Rainy = 1 if weather == 'Rainy' else 0
            Weather_Condition_Sunny = 1 if weather == 'Sunny' else 0

            # Prepare input data as a dictionary
            input_data_dict = {
                'Rainfall_mm': Rainfall_mm,
                'Temperature_Celsius': Temperature_Celsius,
                'Fertilizer_Used': Fertilizer_Used,
                'Irrigation_Used': Irrigation_Used,
                'Days_to_Harvest': Days_to_Harvest,
                'Region_East': Region_East,
                'Region_North': Region_North,
                'Region_South': Region_South,
                'Region_West': Region_West,
                'Soil_Type_Chalky': Soil_Type_Chalky,
                'Soil_Type_Clay': Soil_Type_Clay,
                'Soil_Type_Loam': Soil_Type_Loam,
                'Soil_Type_Peaty': Soil_Type_Peaty,
                'Soil_Type_Sandy': Soil_Type_Sandy,
                'Soil_Type_Silt': Soil_Type_Silt,
                'Crop_Barley': Crop_Barley,
                'Crop_Cotton': Crop_Cotton,
                'Crop_Maize': Crop_Maize,
                'Crop_Rice': Crop_Rice,
                'Crop_Soybean': Crop_Soybean,
                'Crop_Wheat': Crop_Wheat,
                'Weather_Condition_Cloudy': Weather_Condition_Cloudy,
                'Weather_Condition_Rainy': Weather_Condition_Rainy,
                'Weather_Condition_Sunny': Weather_Condition_Sunny
            }

            # Convert input data to pandas DataFrame with feature names
            input_data = pd.DataFrame([input_data_dict], columns=feature_names)

            # Scale the input data using the loaded scaler
            scaled = scaler.transform(input_data)
            
            if Rainfall_mm <= 10 and Irrigation_Used == 0:
                raise ValueError('Yield Not Possible due to Insufficient Water')
            elif Days_to_Harvest <= 30:
                raise ValueError('Yield Not Possible due to Insufficient Growth Period')
            
            # Prediction
            result = model.predict(scaled)[0]
            return render_template('prediction.html', prediction_text=f'{result:.2f} tons per hectare')
        
        except ValueError as e:
            return render_template('index.html', prediction_text=str(e))
    else:
        return render_template('index.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=7002)
