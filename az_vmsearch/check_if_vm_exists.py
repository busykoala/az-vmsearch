from az_vmsearch.cloudprice import VMPrice


def check_if_vm_exists(
    vm_name: str, vm_prices: list[VMPrice]
) -> list[VMPrice]:
    return [vm for vm in vm_prices if vm.name == vm_name]
