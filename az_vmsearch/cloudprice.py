from dataclasses import dataclass
from enum import Enum
from typing import Optional

import requests
from bs4 import BeautifulSoup
from bs4.element import NavigableString


class Currency(Enum):
    USD = "USD"
    EUR = "EUR"
    CHF = "CHF"


@dataclass
class VMPrice:
    name: str
    cpu_cores: int
    memory_gb: float
    linux_price: float
    windows_price: float
    quota: Optional[int] = 0


def get_table_data(html: str) -> list[VMPrice]:
    soup = BeautifulSoup(html, "html.parser")

    table = soup.find("table")
    if not table or isinstance(table, NavigableString):
        return []

    vms = []
    for row in table.find_all("tr"):
        row_list = [val.text for val in row.find_all("td")]
        try:
            vm_price = VMPrice(
                name=row_list[1],
                cpu_cores=int(row_list[2]),
                memory_gb=float(row_list[3]),
                linux_price=float(row_list[4].replace(",", "")),
                windows_price=float("nan")
                if row_list[5] == "n/a"
                else float(row_list[5].replace(",", "")),
            )
            vms.append(vm_price)
        except IndexError:
            pass
    return vms


def get_cloud_prices(
    currency: Currency, region: str, mem: int, cpu: int
) -> list[VMPrice]:
    url = "https://cloudprice.net/"
    params = {
        "currency": currency.value,
        "region": region,
        "timeoption": "month",
        "sortField": "linuxPrice",
        "sortOrder": "true",
        "_memoryInMB_min": mem,
        "_numberOfCores_min": cpu,
    }
    response = requests.get(url, params=params)
    return get_table_data(response.text)
