from unittest.mock import patch

from click.testing import CliRunner

from az_vmsearch.cloudprice import VMPrice
from cli import search_vms


def test_search_vms_success():
    # Mock Config object and results from find_vms
    mock_vms = [
        VMPrice(
            name="Standard_A4_v2",
            cpu_cores=4,
            memory_gb=8,
            linux_price=100.05,
            windows_price=120.50,
            quota=10,
        ),
        VMPrice(
            name="Standard_B4_v2",
            cpu_cores=4,
            memory_gb=16,
            linux_price=110.00,
            windows_price=130.00,
            quota=5,
        ),
    ]

    # Patch find_vms to return mock VMs
    with patch("cli.find_vms", return_value=mock_vms):
        # Use Click's CliRunner to invoke the CLI
        runner = CliRunner()
        result = runner.invoke(
            search_vms,
            [
                "--subscription-id",
                "ca55555-333a-4abe-8b40-6f091cc14b7b",
                "--region",
                "westeurope",
                "--currency",
                "USD",
                "--min-cores",
                "4",
                "--min-memory",
                "8",
                "--limit",
                "1",
            ],
        )

        # Assertions
        assert result.exit_code == 0
        assert "Found 2 VMs. Displaying cheapest 1:" in result.output
        assert "Standard_A4_v2" in result.output
        assert "CPU Cores: 4" not in result.output


def test_search_vms_failure():
    # Patch find_vms to raise an exception
    with patch("cli.find_vms", side_effect=Exception("An error occurred")):
        # Use Click's CliRunner to invoke the CLI
        runner = CliRunner()
        result = runner.invoke(
            search_vms,
            [
                "--subscription-id",
                "ca55555-333a-4abe-8b40-6f091cc14b7b",
                "--region",
                "westeurope",
                "--currency",
                "USD",
                "--min-cores",
                "4",
                "--min-memory",
                "8",
                "--limit",
                "1",
            ],
        )

        # Assertions
        assert result.exit_code != 0
        assert "An error occurred" in result.output

    # Test when find_vms returns an empty list
    with patch("cli.find_vms", return_value=[]):
        runner = CliRunner()
        result = runner.invoke(
            search_vms,
            [
                "--subscription-id",
                "ca283371-879a-4abe-8b40-6f091cc14b7b",
                "--region",
                "westeurope",
                "--currency",
                "USD",
                "--min-cores",
                "4",
                "--min-memory",
                "8",
                "--limit",
                "1",
            ],
        )

        # Assertions
        assert result.exit_code == 0
        assert "Found 0 VMs. Displaying cheapest 1:" in result.output
