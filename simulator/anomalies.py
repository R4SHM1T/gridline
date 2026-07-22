import random

def inject_anomaly(device_id, current_val):
    rand = random.random()
    if rand < 0.01:
        if "temp" in device_id:
            return current_val + 10.0 # Huge spike
        elif "plug" in device_id:
            return 0.0 # Drop to zero
        elif "motion" in device_id:
            return "active" # Stuck active
    return current_val
