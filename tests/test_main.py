from unittest.mock import patch

from az_vmsearch.cloudprice import Currency
from az_vmsearch.cloudprice import VMPrice
from az_vmsearch.main import Config
from az_vmsearch.main import find_vms


def test_find_vms():
    # Mock Config object
    config = Config(
        subscription_id="ca222222-333a-4abe-8b40-6f091cc14b7b",
        region="westeurope",
        currency=Currency.USD,
        min_cores=4,
        min_memory=8,
    )

    # Mock return values for dependent functions
    mock_cloud_prices = [
        VMPrice(
            name="Standard_A4_v2",
            cpu_cores=4,
            memory_gb=8,
            linux_price=100.05,
            windows_price=120.50,
        )
    ]

    mock_quota_data = [
        {"name": "standardAv2Family", "properties": {"limit": {"value": 10}}}
    ]

    mock_vms = [
        {"name": "Standard_A4_v2", "numberOfCores": 4, "memoryInMB": 8192}
    ]

    # Mock create_vm_family to map VM to a family
    def mock_create_vm_family(vm):
        return "standardAv2Family"

    # Mock check_if_vm_exists to simulate VM availability in cloud prices
    def mock_check_if_vm_exists(vm_name, vm_prices):
        return [
            VMPrice(
                name="Standard_A4_v2",
                cpu_cores=4,
                memory_gb=8,
                linux_price=100.05,
                windows_price=120.50,
                quota=0,
            )
        ]

    # Patch the dependent functions using correct import paths
    with patch(
        "az_vmsearch.main.get_cloud_prices", return_value=mock_cloud_prices
    ), patch(
        "az_vmsearch.main.get_quota_data", return_value=mock_quota_data
    ), patch("az_vmsearch.main.get_vms", return_value=mock_vms), patch(
        "az_vmsearch.main.create_vm_family", side_effect=mock_create_vm_family
    ), patch(
        "az_vmsearch.main.check_if_vm_exists",
        side_effect=mock_check_if_vm_exists,
    ):
        # Call the function under test
        result = find_vms(config)

        # Assertions
        assert len(result) == 1
        assert result[0].name == "Standard_A4_v2"
        assert result[0].cpu_cores == 4
        assert result[0].memory_gb == 8
        assert result[0].linux_price == 100.05
        assert result[0].windows_price == 120.50
        assert result[0].quota == 10
