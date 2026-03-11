import pandas as pd
import datetime
from simulator import flash_array_sim, flash_blade_sim
import random

class DataCollector:
    def __init__(self):
        self.historical_data = []

    def generate_historical_data(self, days=30):
        """
        Generate mock historical data for training.
        """
        print(f"Generating {days} days of historical telemetry...")
        
        # Reset simulators for consistent baseline
        flash_array_sim.current_used_tb = flash_array_sim.total_capacity_tb * 0.4
        flash_blade_sim.current_used_tb = flash_blade_sim.total_capacity_tb * 0.3
        
        end_date = datetime.datetime.now()
        start_date = end_date - datetime.timedelta(days=days)
        
        for i in range(days):
            current_date = start_date + datetime.timedelta(days=i)
            
            # FlashArray metrics
            fa_growth = random.uniform(0.2, 1.0)
            flash_array_sim.current_used_tb += fa_growth
            self.historical_data.append({
                "timestamp": current_date.strftime("%Y-%m-%d"),
                "device": "FlashArray",
                "used_capacity_tb": round(flash_array_sim.current_used_tb, 2),
                "total_capacity_tb": flash_array_sim.total_capacity_tb
            })
            
            # FlashBlade metrics
            fb_growth = random.uniform(0.5, 2.5)
            flash_blade_sim.current_used_tb += fb_growth
            self.historical_data.append({
                "timestamp": current_date.strftime("%Y-%m-%d"),
                "device": "FlashBlade",
                "used_capacity_tb": round(flash_blade_sim.current_used_tb, 2),
                "total_capacity_tb": flash_blade_sim.total_capacity_tb
            })
            
    def get_dataframe(self):
        """
        Convert collected historical data to a pandas DataFrame.
        """
        df = pd.DataFrame(self.historical_data)
        # Convert timestamp to datetime and map to an ordinal for linear regression
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['day_index'] = (df['timestamp'] - df['timestamp'].min()).dt.days
        return df

    def get_current_metrics(self):
        """
        Fetch current data from simulators.
        """
        fa_metrics = flash_array_sim.get_capacity_metrics()
        fb_metrics = flash_blade_sim.get_capacity_metrics()
        return fa_metrics, fb_metrics
