import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np

class CapacityPredictor:
    def __init__(self):
        self.models = {}

    def train(self, df: pd.DataFrame):
        """
        Trains a linear regression model for each storage device
        based on historical mock telemetry series.
        """
        print("Training Capacity Prediction Models...")
        for device in df['device'].unique():
            device_data = df[df['device'] == device].copy()
            if device_data.empty:
                continue
            
            # Features: generic day index
            X = device_data[['day_index']]
            # Target: used capacity
            y = device_data['used_capacity_tb']
            
            model = LinearRegression()
            model.fit(X, y)
            
            self.models[device] = {
                "model": model,
                "latest_day_index": device_data['day_index'].max()
            }
            print(f"- {device} model trained. (Coef: {model.coef_[0]:.4f} TB/day)")

    def predict_future_usage(self, device, days_ahead=30):
        """
        Predict what the usage will be 'days_ahead' from the latest data point.
        """
        if device not in self.models:
            print(f"No model trained for {device}")
            return None
            
        model_info = self.models[device]
        model = model_info["model"]
        future_day_index = model_info["latest_day_index"] + days_ahead
        
        # Predict
        predicted_tb = model.predict([[future_day_index]])[0]
        return round(predicted_tb, 2)
