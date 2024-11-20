import json
from unittest.mock import Mock
from unittest.mock import patch

from az_vmsearch.get_quota_data import get_quota_data


def test_get_quota_data_success():
    # Minimal mock data for testing
    mock_stdout = json.dumps(
        [
            {
                "id": "/subscriptions/ca222222-333a-4abe-8b40-6f091cc14b7b/providers/Microsoft.Compute/locations/westeurope/providers/Microsoft.Quota/quotas/standardDDv4Family",
                "name": "standardDDv4Family",
                "properties": {
                    "isQuotaApplicable": True,
                    "limit": {
                        "limitObjectType": "LimitValue",
                        "limitType": "Independent",
                        "value": 10,
                    },
                    "name": {
                        "localizedValue": "Standard DDv4 Family vCPUs",
                        "value": "standardDDv4Family",
                    },
                    "properties": {},
                    "quotaPeriod": None,
                    "resourceType": None,
                    "unit": "Count",
                },
                "type": "Microsoft.Quota/Quotas",
            }
        ]
    )

    # Mock the subprocess.run function
    with patch("subprocess.run") as mocked_run:
        mocked_process = Mock()
        mocked_process.returncode = 0
        mocked_process.stdout = mock_stdout
        mocked_run.return_value = mocked_process

        # Call the function
        result = get_quota_data(
            "westeurope", "ca222222-333a-4abe-8b40-6f091cc14b7b"
        )

        # Assertions
        assert result == json.loads(mock_stdout)
        mocked_run.assert_called_once_with(
            [
                "az",
                "quota",
                "list",
                "--scope",
                "/subscriptions/ca222222-333a-4abe-8b40-6f091cc14b7b/providers/Microsoft.Compute/locations/westeurope",
                "--output",
                "json",
            ],
            capture_output=True,
            text=True,
        )


def test_get_quota_data_error():
    # Mock the subprocess.run function to simulate an error
    with patch("subprocess.run") as mocked_run:
        mocked_process = Mock()
        mocked_process.returncode = 1
        mocked_process.stderr = "An error occurred"
        mocked_run.return_value = mocked_process

        # Call the function
        result = get_quota_data(
            "westeurope", "ca222222-333a-4abe-8b40-6f091cc14b7b"
        )

        # Assertions
        assert result == []
        mocked_run.assert_called_once_with(
            [
                "az",
                "quota",
                "list",
                "--scope",
                "/subscriptions/ca222222-333a-4abe-8b40-6f091cc14b7b/providers/Microsoft.Compute/locations/westeurope",
                "--output",
                "json",
            ],
            capture_output=True,
            text=True,
        )
