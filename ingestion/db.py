import os
import psycopg2
from psycopg2.extras import execute_values
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    return psycopg2.connect(
        host=os.getenv("POSTGRES_HOST", "localhost"),
        port=os.getenv("POSTGRES_PORT", "5432"),
        dbname=os.getenv("POSTGRES_DB", "gridline"),
        user=os.getenv("POSTGRES_USER", "gridline"),
        password=os.getenv("POSTGRES_PASSWORD", "gridline")
    )

def setup_schema():
    conn = get_connection()
    cur = conn.cursor()
    
    # Create raw schema if not exists
    cur.execute("CREATE SCHEMA IF NOT EXISTS raw;")
    
    # Devices table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS raw.devices (
            device_id VARCHAR PRIMARY KEY,
            label VARCHAR,
            room VARCHAR,
            type VARCHAR,
            capabilities JSONB
        );
    """)
    
    # Device events table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS raw.device_events (
            event_id SERIAL PRIMARY KEY,
            device_id VARCHAR,
            capability VARCHAR,
            attribute VARCHAR,
            value VARCHAR,
            unit VARCHAR,
            ts TIMESTAMP,
            ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    
    conn.commit()
    cur.close()
    conn.close()
    print("Schema setup complete.")

if __name__ == "__main__":
    setup_schema()
