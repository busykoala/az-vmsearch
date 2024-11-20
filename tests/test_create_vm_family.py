from az_vmsearch.create_vm_family import create_vm_family


def test_create_vm_family():
    # Test Case 1: Valid VM name
    vm = {"name": "Standard_A8_v2"}
    result = create_vm_family(vm)
    assert (
        result == "standardAv2Family"
    ), f"Expected 'standardAFamilyv2' but got {result}"

    # Test Case 2: Valid VM name with different family
    vm = {"name": "Standard_D4_v5"}
    result = create_vm_family(vm)
    assert (
        result == "standardDv5Family"
    ), f"Expected 'standardDFamilyv5' but got {result}"

    # Test Case 3: Missing "name" key
    vm = {}
    result = create_vm_family(vm)
    assert result == "", f"Expected an empty string but got {result}"
