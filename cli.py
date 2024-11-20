from pprint import pprint

import click

from az_vmsearch.cloudprice import Currency
from az_vmsearch.main import Config
from az_vmsearch.main import find_vms


@click.command()
@click.option(
    "--subscription-id",
    required=True,
    help="Azure subscription ID.",
)
@click.option(
    "--region",
    required=True,
    help="Azure region to search for VMs. Default is 'westeurope'.",
)
@click.option(
    "--currency",
    default="USD",
    type=click.Choice([e.name for e in Currency], case_sensitive=False),
    help="Currency for pricing. Default is 'USD'.",
)
@click.option(
    "--min-cores",
    default=4,
    type=int,
    help="Minimum number of CPU cores. Default is 4.",
)
@click.option(
    "--min-memory",
    default=8,
    type=int,
    help="Minimum memory (in GB). Default is 8.",
)
@click.option(
    "--limit",
    default=5,
    type=int,
    help="Limit the number of VMs displayed. Default is 5.",
)
def search_vms(
    subscription_id, region, currency, min_cores, min_memory, limit
):
    """
    CLI to search for Azure VMs based on specified criteria.
    """
    # Create configuration
    config = Config(
        subscription_id=subscription_id,
        region=region,
        currency=Currency[currency],
        min_cores=min_cores,
        min_memory=min_memory,
    )

    # Find VMs
    vms = find_vms(config)
    click.echo(f"Found {len(vms)} VMs. Displaying cheapest {limit}:\n")
    for vm in vms[:limit]:
        pprint(vm)


if __name__ == "__main__":
    search_vms()
