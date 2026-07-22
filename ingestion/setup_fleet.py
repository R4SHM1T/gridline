import os
import yaml
import requests
from dotenv import load_dotenv

load_dotenv()

PAT = os.getenv("SMARTTHINGS_PAT")
HEADERS = {
    "Authorization": f"Bearer {PAT}",
    "Content-Type": "application/json"
}
BASE_URL = "https://api.smartthings.com/v1"

def load_fleet():
    with open("../config/fleet.yaml", "r") as f:
        return yaml.safe_load(f)["fleet"]

def get_location_id():
    # Fetch first location to create devices in
    res = requests.get(f"{BASE_URL}/locations", headers=HEADERS)
    res.raise_for_status()
    locations = res.json().get("items", [])
    if not locations:
        raise Exception("No locations found in SmartThings account.")
    return locations[0]["locationId"]

def create_virtual_device(location_id, device):
    payload = {
        "label": device["id"],
        "locationId": location_id,
        "app": {
            "profileId": get_profile_id_for_type(device["type"])
        }
    }
    # For a real implementation, you'd create device profiles first, 
    # but the SmartThings API allows creating virtual devices with standard profiles.
    # We will simulate the setup or print instructions if this needs a manual step or specific profile IDs.
    print(f"Would create device: {device['id']} of type {device['type']}")
    # res = requests.post(f"{BASE_URL}/devices", json=payload, headers=HEADERS)
    # return res.json()

def get_profile_id_for_type(device_type):
    # Mocking profile IDs for now. In reality, you'd query profiles or create them.
    return "mock-profile-id"

if __name__ == "__main__":
    print("This script will set up the virtual fleet in SmartThings.")
    # loc = get_location_id()
    # fleet = load_fleet()
    # for dev in fleet:
    #     create_virtual_device(loc, dev)
    print("Setup script ready.")
