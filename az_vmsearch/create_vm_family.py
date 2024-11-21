import re
from dataclasses import dataclass
from typing import Optional

from az_vmsearch.data.regions import regions
from az_vmsearch.data.types import vm_type_properties


@dataclass
class VMProperties:
    details: dict[str, Optional[str]]
    region_name: Optional[str]
    region_code: str
    version: str


def get_vm_properties(vm: dict, region: str) -> Optional[VMProperties]:
    vm_name = vm.get("name")
    if not vm_name:
        return
    vm_name = vm_name.split("_")
    version = vm_name[-1]
    family = vm_name[1]
    family_non_numeric_characters = re.sub(r"\d", "", family)
    details = {
        prop: vm_type_properties.get(prop)
        for prop in family_non_numeric_characters
    }
    region_name = regions.get(region)

    return VMProperties(
        details=details,
        region_name=region_name,
        region_code=region,
        version=version,
    )


def create_vm_family(vm: dict) -> str:
    vm_name = vm.get("name")
    if not vm_name:
        return ""
    vm_name = vm_name.split("_")
    version = vm_name[-1]
    family = vm_name[1]
    family_non_numeric_characters = re.sub(r"\d", "", family)
    return f"standard{family_non_numeric_characters.upper()}{version}Family"
