import os
import requests

def agent_action(device_id, command):
    print(f"Agent executes '{command}' on {device_id}")
    return True

if __name__ == "__main__":
    agent_action("motion_living_room", "turn_on")
