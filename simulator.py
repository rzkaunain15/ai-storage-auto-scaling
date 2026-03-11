import random
import datetime

class PureStorageSimulator:
    """
    Simulates Pure Storage FlashArray and FlashBlade REST APIs for capacity planning.
    """
    def __init__(self, device_type="FlashArray", total_capacity_tb=100.0):
        self.device_type = device_type
        self.total_capacity_tb = total_capacity_tb
        # Start at 50% capacity
        self.current_used_tb = total_capacity_tb * 0.5
    
    def get_capacity_metrics(self):
        """
        Simulate an API call returning current capacity metrics.
        Returns a dictionary with used, total, and timestamp.
        """
        # Introduce a little noise but generally increasing trend
        growth = random.uniform(0.1, 0.5) 
        self.current_used_tb += growth
        
        # Cap at total
        self.current_used_tb = min(self.current_used_tb, self.total_capacity_tb)
        
        return {
            "device": self.device_type,
            "timestamp": datetime.datetime.now().isoformat(),
            "used_capacity_tb": round(self.current_used_tb, 2),
            "total_capacity_tb": round(self.total_capacity_tb, 2),
            "utilization_percentage": round((self.current_used_tb / self.total_capacity_tb) * 100, 2)
        }

    def expand_volume(self, add_tb):
        """
        Simulate an API call to expand a volume or add capacity.
        """
        print(f"[API Simulate] Expanding {self.device_type} capacity by {add_tb} TB...")
        self.total_capacity_tb += add_tb
        print(f"[API Simulate] New Total Capacity: {round(self.total_capacity_tb, 2)} TB")
        return True

# Initialize simulators
flash_array_sim = PureStorageSimulator(device_type="FlashArray", total_capacity_tb=100.0)
flash_blade_sim = PureStorageSimulator(device_type="FlashBlade", total_capacity_tb=250.0)
