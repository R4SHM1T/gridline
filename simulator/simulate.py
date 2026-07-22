import time
import datetime
import json
import random
import sys
from pathlib import Path

# Adjust path to import from ingestion if needed
sys.path.append(str(Path(__file__).parent.parent))

from rhythms import apply_time_of_day, motion_probability, temperature_drift
from anomalies import inject_anomaly

def simulate_device_tick(device, ts):
    state = "baseline"
    hour = ts.hour
    day = ts.weekday()
    time_state = apply_time_of_day(hour, day)
    
    val = None
    if device["type"] == "motionSensor":
        prob = motion_probability(time_state)
        val = "active" if random.random() < prob else "inactive"
    elif device["type"] == "temperatureMeasurement":
        val = temperature_drift(hour) + random.uniform(-0.5, 0.5)
    elif device["type"] == "powerMeter":
        val = 100.0 if time_state in ["morning_peak", "evening_peak"] else 10.0
    elif device["type"] == "contactSensor":
        val = "open" if random.random() < 0.05 else "closed"
    else:
        val = "on" if random.random() < 0.5 else "off"

    val = inject_anomaly(device["id"], val)
    return val

def run_simulation(fleet):
    print("Running simulator tick...")
    now = datetime.datetime.now()
    for d in fleet:
        val = simulate_device_tick(d, now)
        print(f"Device {d['id']} simulated value: {val}")

if __name__ == "__main__":
    import yaml
    with open("../config/fleet.yaml") as f:
        fleet = yaml.safe_load(f)["fleet"]
    run_simulation(fleet)
