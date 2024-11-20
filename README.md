# Azure VM Search Utility

The mapping in azure between VM families and VM types is not always clear.
To get a cheap option that is available in a subscription quota in a region
this utility can be used.

The tool is using the price list by `cloudprice.net` to get the VM prices.
The prices are used to determine which VMs are available in a subscription
quota in a specific region.

## Usage

```bash
git clone https://github.com/busykoala/az-vmsearch.git
cd az-vmsearch
poetry install
poetry run python cli.py --help
```

## Development

```bash
poetry run ruff format
poetry run ruff check --fix
```
