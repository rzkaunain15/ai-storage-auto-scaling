import smtplib
from email.mime.text import MIMEText
from simulator import flash_array_sim, flash_blade_sim

class AutomationEngine:
    def __init__(self, admin_email="rzkaunain@gmail.com"):
        self.admin_email = admin_email
        self.threshold_percent = 85.0 # Trigger expansion if > 85%

    def check_and_automate(self, current_metrics, predictions, days_ahead):
        """
        Check predictions against the total capacity.
        If predicted utilization exceeds 85%, trigger expansion and alert.
        """
        print("\n--- Running Automation Engine ---")
        
        # Map device names to the simulator instances for expansion
        simulators = {
            "FlashArray": flash_array_sim,
            "FlashBlade": flash_blade_sim
        }

        for metric in current_metrics:
            device = metric['device']
            current_used = metric['used_capacity_tb']
            total_cap = metric['total_capacity_tb']
            
            # Get the prediction
            predicted_used = predictions.get(device)
            if not predicted_used:
                continue
                
            predicted_utilization = (predicted_used / total_cap) * 100
            
            print(f"[{device}] Current Util: {(current_used/total_cap)*100:.1f}%")
            print(f"[{device}] Predicted Util in {days_ahead} days: {predicted_utilization:.1f}%")
            
            if predicted_utilization >= self.threshold_percent:
                print(f"[{device}] THRESHOLD EXCEEDED ({predicted_utilization:.1f}% >= {self.threshold_percent}%).")
                self._trigger_expansion(simulators[device], device, predicted_used_tb=predicted_used, total_tb=total_cap)
            else:
                print(f"[{device}] Capacity looks healthy.")

    def _trigger_expansion(self, simulator, device_name, predicted_used_tb, total_tb):
        """
        Calculates expansion amount and calls the simulator API.
        Then sends an email alert.
        """
        # Expand by 50% of current total capacity as a simple rule
        add_tb = round(total_tb * 0.5, 2)
        
        success = simulator.expand_volume(add_tb)
        if success:
            new_total = total_tb + add_tb
            self.send_email_alert(device_name, predicted_used_tb, total_tb, new_total)
            
    def send_email_alert(self, device_name, predicted_tb, old_total_tb, new_total_tb):
        """
        Logs the email alert that would be sent via SMTP to the administrator.
        """
        subject = f"URGENT: Automated Capacity Expansion for {device_name}"
        body = (
            f"Automated System Alert\n"
            f"----------------------------------------\n"
            f"Device: {device_name}\n"
            f"Prediction: Usage predicted to hit {predicted_tb} TB in the near future.\n"
            f"Previous Total Capacity: {old_total_tb} TB\n"
            f"Action Taken: Automatically expanded volume/hardware by {round(new_total_tb - old_total_tb, 2)} TB.\n"
            f"New Total Capacity: {new_total_tb} TB\n\n"
            f"Please verify this change in the Pure Storage management console.\n"
        )
        
        print("\n[EMAIL OUTBOX]")
        print(f"To: {self.admin_email}")
        print(f"Subject: {subject}")
        print(f"Body:\n{body}")
        
        # Note: Actual SMTP implementation would go here (requires credentials).
        # msg = MIMEText(body)
        # msg['Subject'] = subject
        # msg['From'] = "admin@storage-ai.sys"
        # msg['To'] = self.admin_email
        # with smtplib.SMTP('localhost') as server: # Or real SMTP server
        #     server.send_message(msg)
