import json
import subprocess


def get_quota_data(location: str, subscription_id: str) -> list[dict]:
    result = subprocess.run(
        [
            "az",
            "quota",
            "list",
            "--scope",
            f"/subscriptions/{subscription_id}/providers/Microsoft.Compute/locations/{location}",
            "--output",
            "json",
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print("Error fetching quota data:", result.stderr)
        return []
    return json.loads(result.stdout)
