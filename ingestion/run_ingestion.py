import json
import datetime
from db import get_connection
from poll_status import fetch_devices, poll_device_status

def sync_devices_to_db(conn, devices):
    cur = conn.cursor()
    for d in devices:
        cur.execute("""
            INSERT INTO raw.devices (device_id, label, room, type, capabilities)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (device_id) DO UPDATE SET
                label = EXCLUDED.label,
                room = EXCLUDED.room,
                type = EXCLUDED.type,
                capabilities = EXCLUDED.capabilities;
        """, (
            d["deviceId"],
            d.get("label", "Unknown"),
            d.get("roomId", "Unknown"),
            d.get("deviceTypeName", "Unknown"),
            json.dumps(d.get("components", {}))
        ))
    conn.commit()
    cur.close()

def ingest_status_events(conn, devices):
    cur = conn.cursor()
    for d in devices:
        device_id = d["deviceId"]
        status = poll_device_status(device_id)
        
        main_comp = status.get("components", {}).get("main", {})
        for capability, attrs in main_comp.items():
            for attr_name, attr_data in attrs.items():
                if isinstance(attr_data, dict) and "value" in attr_data:
                    val = str(attr_data["value"])
                    unit = attr_data.get("unit", "")
                    ts = attr_data.get("timestamp", datetime.datetime.utcnow().isoformat())
                    
                    # Basic parsing to handle smartthings iso timestamps
                    try:
                        ts = datetime.datetime.strptime(ts[:19], "%Y-%m-%dT%H:%M:%S")
                    except ValueError:
                        ts = datetime.datetime.utcnow()

                    cur.execute("""
                        INSERT INTO raw.device_events (device_id, capability, attribute, value, unit, ts)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """, (device_id, capability, attr_name, val, unit, ts))
    conn.commit()
    cur.close()

def run():
    print("Connecting to DB...")
    conn = get_connection()
    
    print("Fetching devices from SmartThings...")
    devices = fetch_devices()
    print(f"Found {len(devices)} devices.")
    
    print("Syncing devices table...")
    sync_devices_to_db(conn, devices)
    
    print("Polling status and writing events...")
    ingest_status_events(conn, devices)
    
    print("Ingestion complete.")
    conn.close()

if __name__ == "__main__":
    run()
