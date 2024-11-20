import re


def create_vm_family(vm: dict) -> str:
    vm_name = vm.get("name")
    if not vm_name:
        return ""
    vm_name = vm_name.split("_")
    version = vm_name[-1]
    family = vm_name[1]
    family_non_numeric_characters = re.sub(r"\d", "", family)
    return f"standard{family_non_numeric_characters.upper()}{version}Family"
