from data_collector import DataCollector
from model import CapacityPredictor
from automation import AutomationEngine

def main():
    print("=====================================================")
    print("  AI-Driven Storage Capacity Prediction Auto-Scaling ")
    print("=====================================================")
    
    # 1. Collect Data
    collector = DataCollector()
    collector.generate_historical_data(days=60) # Generate 60 days of data
    df = collector.get_dataframe()
    
    print(f"\nCollected {len(df)} historical data points.")
    
    # 2. Train Model
    predictor = CapacityPredictor()
    predictor.train(df)
    
    # 3. Simulate getting current metrics
    current_metrics = list(collector.get_current_metrics())
    
    # 4. Predict Future
    days_to_predict = 30
    predictions = {}
    print(f"\n--- Predicting Usage for Next {days_to_predict} Days ---")
    for device in df['device'].unique():
        pred = predictor.predict_future_usage(device, days_ahead=days_to_predict)
        predictions[device] = pred
        print(f"{device} predicted usage: {pred} TB")
        
    # 5. Automation & Alerting
    automation = AutomationEngine(admin_email="rzkaunain@gmail.com")
    automation.check_and_automate(current_metrics, predictions, days_ahead=days_to_predict)

if __name__ == "__main__":
    main()
