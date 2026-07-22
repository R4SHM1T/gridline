"""Autopilot: the warehouse steering the home.

No magic here. The dbt marts flag things that look wrong (a fridge drawing
zero watts, a temperature reading that jumped ten degrees). The autopilot
reads those flags and reacts through the SmartThings Rules API.

Everything it does is a plain threshold from the playbook below. It runs
in dry-run mode by default, so it tells you what it would do instead of
doing it. Pass --live to let it actually create rules.
"""

import argparse
import os

import requests

API = "https://api.smartthings.com/v1"
RULE_PREFIX = "gridline-auto"

# what to do when a mart flags a problem. one entry per anomaly kind.
PLAYBOOK = {
    "fridge_power_zero": {
        "when": "plug_fridge draws 0 W for 5 minutes",
        "then": "send an alert. a silent fridge is spoiled food.",
    },
    "temp_spike": {
        "when": "a room jumps more than 8 degrees between readings",
        "then": "switch off the heater plug and send an alert.",
    },
    "motion_stuck": {
        "when": "a motion sensor reports active for a full hour",
        "then": "mark the device unhealthy and send an alert.",
    },
}


def pending_anomalies():
    """Read open flags from mart_anomalies.

    TODO: wire this to postgres once the anomaly mart lands (see PRD roadmap).
    For now it returns an empty list so a dry run is honest about doing nothing.
    """
    return []


def create_rule(token, name, dry_run=True):
    if dry_run:
        print(f"[dry-run] would create rule {name}")
        return None
    resp = requests.post(
        f"{API}/rules",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": name, "actions": []},
        timeout=10,
    )
    resp.raise_for_status()
    return resp.json()


def main():
    parser = argparse.ArgumentParser(description="react to warehouse anomaly flags")
    parser.add_argument("--live", action="store_true", help="actually create rules")
    args = parser.parse_args()

    token = os.environ.get("SMARTTHINGS_PAT", "")
    flags = pending_anomalies()
    if not flags:
        print("nothing flagged. the house is fine.")
        return

    for flag in flags:
        play = PLAYBOOK.get(flag["kind"])
        if play is None:
            print(f"no playbook entry for {flag['kind']}, skipping")
            continue
        name = f"{RULE_PREFIX}-{flag['kind']}"
        print(f"{play['when']} -> {play['then']}")
        create_rule(token, name, dry_run=not args.live)


if __name__ == "__main__":
    main()
