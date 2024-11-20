import json
import subprocess


def get_vms(location: str) -> list[dict]:
    result = subprocess.run(
        ["az", "vm", "list-sizes", "--location", location, "--output", "json"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print("Error fetching VM data:", result.stderr)
        return []
    return json.loads(result.stdout)
