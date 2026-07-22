import os
import requests
from dotenv import load_dotenv

load_dotenv()

PAT = os.getenv("SMARTTHINGS_PAT")
HEADERS = {
    "Authorization": f"Bearer {PAT}",
    "Content-Type": "application/json"
}
BASE_URL = "https://api.smartthings.com/v1"

def fetch_devices():
    res = requests.get(f"{BASE_URL}/devices", headers=HEADERS)
    if res.status_code != 200:
        print(f"Failed to fetch devices: {res.text}")
        return []
    return res.json().get("items", [])

def poll_device_status(device_id):
    res = requests.get(f"{BASE_URL}/devices/{device_id}/status", headers=HEADERS)
    if res.status_code != 200:
        print(f"Failed to fetch status for {device_id}: {res.text}")
        return {}
    return res.json()

if __name__ == "__main__":
    devices = fetch_devices()
    print(f"Found {len(devices)} devices.")
    for d in devices:
        status = poll_device_status(d["deviceId"])
        print(f"Status for {d['label']}: {status.get('components', {}).get('main', {}).keys()}")
