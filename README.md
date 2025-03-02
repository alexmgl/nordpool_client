# Nordpool Client

A Python client to fetch, process, and analyze Nordpool electricity market data by interacting with the Nordpool Data Portal API.

## Overview

The Nordpool Client provides an easy-to-use interface for retrieving various types of electricity market data, including:

- **Auction Data**: Retrieve auction configurations and latest auction availability.
- **Day-Ahead Prices**: Get day-ahead prices for multiple delivery areas.
- **Price Histories & Aggregated Data**: Fetch historical price data and aggregated price statistics.
- **Intraday Market Statistics**: Access hourly and daily intraday market statistics.
- **EPAD Data**: Retrieve EPAD auction results and bid curves.
- **System Prices, Flows, Consumption, & Production**: Query system price data, physical flows, consumption, and production data.

## Project Structure

```
nordpool-client/
├── pyproject.toml
├── README.md
└── src/
    └── nordpool/
        ├── __init__.py   # Contains: from .client import NordpoolClient
        └── client.py     # Contains the NordpoolClient class implementation
```

## Installation

This project requires Python 3.7 or later.

### Clone the Repository:

```bash
git clone <repository_url>
cd nordpool-client
```

### Install Dependencies:

If you're using pip:

```bash
pip install -r requirements.txt
```

Or if you use Poetry:

```bash
poetry install
```

## Usage

Below is an example of how to use the client:

```python
from nordpool.client import NordpoolClient
from datetime import date

# Instantiate the client
client = NordpoolClient()

# Retrieve day-ahead prices for Finland (FI) and Norway (NO1)
prices = client.get_day_ahead_prices(query_date=date.today(), delivery_areas=["FI", "NO1"], currency="EUR")
print(prices)

# Retrieve and save auction data availability to a JSON file
auction_config = client.get_auction_data_availability(save=True)
```

When the `save` parameter is set to `True`, the response will be saved as a JSON file in the same directory as the script (e.g., `AuctionDataAvailability.json`).

## API Methods

The `NordpoolClient` class provides several methods to access data endpoints. Some key methods include:

### Auction Data:

- `get_auction_data_availability(save=False, **kwargs)`
- `get_auction_data_availability_latest(save=False, **kwargs)`

### Day-Ahead Prices:

- `get_day_ahead_prices(query_date, delivery_areas, currency="EUR", market="DayAhead", **kwargs)`
- `get_single_area_price_history(query_date, delivery_area, currency="EUR", market="DayAhead", **kwargs)`

### Aggregated Prices:

- `get_aggregate_prices(year, delivery_areas, currency="EUR", market="DayAhead", **kwargs)`
- `get_annual_aggregate_prices(delivery_areas, currency="EUR", market="DayAhead", **kwargs)`

### System & Intraday Data:

- `get_system_price(query_date, currency="EUR", **kwargs)`
- `get_intraday_market_statistics(query_date, delivery_area, **kwargs)`
- `get_intraday_hourly_statistics(query_date, delivery_area, **kwargs)`

### EPAD Data:

- `get_epad_results(query_date, **kwargs)`
- `get_epad_yearly_results(year, **kwargs)`
- `get_epad_bid_curves(query_date, **kwargs)`
- `get_epad_yearly_bid_curves(year, **kwargs)`

### Other Data:

- `get_day_ahead_volumes(query_date, delivery_areas, market="DayAhead", **kwargs)`
- `get_day_ahead_capacities(query_date, delivery_area, market="DayAhead", **kwargs)`
- `get_day_ahead_flow(query_date, delivery_area, market="DayAhead", **kwargs)`
- `get_aggregated_bid_curves(query_date, market_code, cluster_name, **kwargs)`
- `get_scheduled_physical_flows(query_date, delivery_area, market="DayAhead", **kwargs)`
- `get_flow_based_constraints(query_date, flow_based_domain, market="DayAhead", **kwargs)`
- `get_manual_frequency_restoration_reserve(query_date, delivery_areas, **kwargs)`
- `get_consumption(query_date, delivery_areas, locations=None, **kwargs)`
- `get_consumption_forecast(query_date, delivery_areas, locations=None, **kwargs)`
- `get_production(query_date, delivery_area, location="", **kwargs)`
- `get_physical_flows(query_date, delivery_area, **kwargs)`

For full details on each method, please refer to the inline documentation within the source code (`client.py`).

## Configuration

The client is configured to use the Nordpool Data Portal API endpoint:

```
https://dataportal-api.nordpoolgroup.com/api
```

No additional API key is required, but you must have an active internet connection.

## Contributing

Contributions are welcome. Feel free to fork the repository, submit issues, and create pull requests.

## License

This project is licensed under the MIT License.