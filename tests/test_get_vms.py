import json
from unittest.mock import Mock
from unittest.mock import patch

from az_vmsearch.get_vms import get_vms


def test_get_vms_success():
    # Mock data returned by the subprocess
    mock_stdout = json.dumps(
        [
            {
                "maxDataDiskCount": 16,
                "memoryInMB": 65536,
                "name": "Standard_A8m_v2",
                "numberOfCores": 8,
                "osDiskSizeInMB": 1047552,
                "resourceDiskSizeInMB": 81920,
            },
            {
                "maxDataDiskCount": 16,
                "memoryInMB": 16384,
                "name": "Standard_A8_v2",
                "numberOfCores": 8,
                "osDiskSizeInMB": 1047552,
                "resourceDiskSizeInMB": 81920,
            },
        ]
    )

    # Mock the subprocess.run function
    with patch("subprocess.run") as mocked_run:
        mocked_process = Mock()
        mocked_process.returncode = 0
        mocked_process.stdout = mock_stdout
        mocked_run.return_value = mocked_process

        # Call the function
        result = get_vms("westeurope")

        # Assertions
        assert result == json.loads(mock_stdout)
        mocked_run.assert_called_once_with(
            [
                "az",
                "vm",
                "list-sizes",
                "--location",
                "westeurope",
                "--output",
                "json",
            ],
            capture_output=True,
            text=True,
        )


def test_get_vms_error():
    # Mock the subprocess.run function to simulate an error
    with patch("subprocess.run") as mocked_run:
        mocked_process = Mock()
        mocked_process.returncode = 1
        mocked_process.stderr = "An error occurred"
        mocked_run.return_value = mocked_process

        # Call the function
        result = get_vms("westeurope")

        # Assertions
        assert result == []
        mocked_run.assert_called_once_with(
            [
                "az",
                "vm",
                "list-sizes",
                "--location",
                "westeurope",
                "--output",
                "json",
            ],
            capture_output=True,
            text=True,
        )
