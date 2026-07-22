import datetime
import random

def apply_time_of_day(hour, day_of_week):
    # morning peak 7-9am, evening 6-9pm
    is_weekend = day_of_week >= 5
    if 7 <= hour <= 9 and not is_weekend:
        return "morning_peak"
    elif 18 <= hour <= 21:
        return "evening_peak"
    return "baseline"

def motion_probability(time_state):
    if time_state == "morning_peak": return 0.7
    elif time_state == "evening_peak": return 0.8
    else: return 0.1

def temperature_drift(hour):
    # coldest at 4am, hottest at 3pm
    base = 20.0
    if hour < 4:
        return base - (4 - hour) * 0.5
    elif hour < 15:
        return base - 2.0 + (hour - 4) * 0.8
    else:
        return base + 6.8 - (hour - 15) * 0.6
