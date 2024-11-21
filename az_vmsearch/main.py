from dataclasses import dataclass

from az_vmsearch.check_if_vm_exists import check_if_vm_exists
from az_vmsearch.cloudprice import Currency
from az_vmsearch.cloudprice import VMPrice
from az_vmsearch.cloudprice import get_cloud_prices
from az_vmsearch.create_vm_family import create_vm_family
from az_vmsearch.get_quota_data import get_quota_data
from az_vmsearch.get_vms import get_vms


@dataclass
class Config:
    subscription_id: str
    region: str
    currency: Currency
    min_cores: int
    min_memory: int


def find_vms(config: Config) -> list[VMPrice]:
    cloud_prices = get_cloud_prices(
        config.currency, config.region, config.min_cores, config.min_memory
    )

    quota_data = get_quota_data(config.region, config.subscription_id)

    vms = get_vms(config.region)

    available_vms = []
    for vm in vms:
        vm_family = create_vm_family(vm)
        if not vm_family:
            continue

        quota = [q for q in quota_data if q.get("name") == vm_family]

        if len(quota) == 1:
            quota_num = (
                quota[0].get("properties", {}).get("limit", {}).get("value", 0)
            )
            if quota_num > 0:
                existing_vms = check_if_vm_exists(
                    vm.get("name", ""), cloud_prices
                )
                for v in existing_vms:
                    v.quota = quota_num
                available_vms.extend(existing_vms)

    return sorted(available_vms, key=lambda x: x.linux_price)
