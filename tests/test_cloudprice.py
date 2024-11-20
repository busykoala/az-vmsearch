from az_vmsearch.cloudprice import Currency
from az_vmsearch.cloudprice import get_cloud_prices
from az_vmsearch.cloudprice import get_table_data


def test_get_table_data():
    # Sample HTML to simulate the table structure
    html = """
    <table>
        <tr>
            <td>1</td>
            <td>Standard_A4_v2</td>
            <td>4</td>
            <td>8</td>
            <td>100.05</td>
            <td>120.50</td>
        </tr>
        <tr>
            <td>2</td>
            <td>Standard_B4_v2</td>
            <td>4</td>
            <td>16</td>
            <td>110.00</td>
            <td>n/a</td>
        </tr>
    </table>
    """

    # Call the function
    vms = get_table_data(html)

    # Assert results
    assert len(vms) == 2

    # Validate the first VM
    assert vms[0].name == "Standard_A4_v2"
    assert vms[0].cpu_cores == 4
    assert vms[0].memory_gb == 8
    assert vms[0].linux_price == 100.05
    assert vms[0].windows_price == 120.50

    # Validate the second VM
    assert vms[1].name == "Standard_B4_v2"
    assert vms[1].cpu_cores == 4
    assert vms[1].memory_gb == 16
    assert vms[1].linux_price == 110.00
    assert vms[1].windows_price != vms[1].windows_price  # Check for NaN


def test_get_cloud_prices(requests_mock):
    # Mocked HTML response
    html = """
    <table>
        <tr>
            <td>1</td>
            <td>Standard_A4_v2</td>
            <td>4</td>
            <td>8</td>
            <td>100.05</td>
            <td>120.50</td>
        </tr>
        <tr>
            <td>2</td>
            <td>Standard_B4_v2</td>
            <td>4</td>
            <td>16</td>
            <td>110.00</td>
            <td>n/a</td>
        </tr>
    </table>
    """

    # Mock the request
    requests_mock.get("https://cloudprice.net/", text=html)

    # Call the function
    vms = get_cloud_prices(Currency.USD, "westeurope", mem=8, cpu=4)

    # Assert results
    assert len(vms) == 2

    # Validate the first VM
    assert vms[0].name == "Standard_A4_v2"
    assert vms[0].cpu_cores == 4
    assert vms[0].memory_gb == 8
    assert vms[0].linux_price == 100.05
    assert vms[0].windows_price == 120.50

    # Validate the second VM
    assert vms[1].name == "Standard_B4_v2"
    assert vms[1].cpu_cores == 4
    assert vms[1].memory_gb == 16
    assert vms[1].linux_price == 110.00
    assert vms[1].windows_price != vms[1].windows_price  # Check for NaN
