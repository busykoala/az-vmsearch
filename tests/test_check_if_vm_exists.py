from az_vmsearch.cloudprice import VMPrice
from az_vmsearch.main import check_if_vm_exists


def test_check_if_vm_exists():
    # Sample data
    vm_prices = [
        VMPrice(
            name="Standard_A4_v2",
            cpu_cores=4,
            memory_gb=8,
            linux_price=100.05,
            windows_price=120.50,
        ),
        VMPrice(
            name="Standard_B4_v2",
            cpu_cores=4,
            memory_gb=16,
            linux_price=110.00,
            windows_price=130.00,
        ),
        VMPrice(
            name="Standard_D4_v2",
            cpu_cores=8,
            memory_gb=32,
            linux_price=150.00,
            windows_price=170.00,
        ),
    ]

    # Test for existing VM
    result = check_if_vm_exists("Standard_A4_v2", vm_prices)
    assert len(result) == 1
    assert result[0].name == "Standard_A4_v2"

    # Test for non-existing VM
    result = check_if_vm_exists("Standard_X1_v2", vm_prices)
    assert len(result) == 0

    # Test for multiple matches
    vm_prices.append(
        VMPrice(
            name="Standard_A4_v2",
            cpu_cores=4,
            memory_gb=8,
            linux_price=100.05,
            windows_price=120.50,
        )
    )
    result = check_if_vm_exists("Standard_A4_v2", vm_prices)
    assert len(result) == 2
    assert all(vm.name == "Standard_A4_v2" for vm in result)
