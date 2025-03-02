# Nordpool Client

A Python client to fetch, process, and analyze Nordpool electricity market data by interacting with the Nordpool Data Portal API.

![Language](https://img.shields.io/badge/language-Python-blue)
![Version](https://img.shields.io/badge/version-v1.0.0-brightgreen)
![License](https://img.shields.io/badge/license-MIT-orange)
![Python Version](https://img.shields.io/badge/python-%3E%3D3.6-informational)

## Overview

The Nordpool Client provides an easy-to-use interface for retrieving various types of Nordpool electricity market data, including:

- **Auction Data**: Retrieve auction configurations and latest auction availability.
- **Day-Ahead Prices**: Get day-ahead prices for multiple delivery areas.
- **Price Histories & Aggregated Data**: Fetch historical price data and aggregated price statistics.
- **Intraday Market Statistics**: Access hourly and daily intraday market statistics.
- **EPAD Data**: Retrieve Elspot Price Auction Data auction results and bid curves.
- **System Prices, Flows, Consumption, & Production**: Query system price data, physical flows, consumption, and production data.

## Disclaimers

- This project is not officially affiliated with or endorsed by Nordpool Group. It is an independent client implementation for accessing publicly available API endpoints.
- The use of Nordpool data may be subject to Nordpool's terms of service and data usage policies. Users of this library are responsible for ensuring their usage complies with Nordpool's terms.
- This client accesses a Nordpool Data API, and usage may be subject to rate limiting or access restrictions imposed by Nordpool.
- Data retrieved through this client should be used in accordance with applicable laws and regulations regarding market data usage.
- The library author is not responsible for any misuse of the data or violations of Nordpool's terms of service.

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

## Installation

Install directly from GitHub using pip:

```bash
pip install git+https://github.com/alexmgl/nordpool_client.git
```

Or clone the repository and install locally:

```bash
git clone https://github.com/alexmgl/nordpool_client.git
cd nordpool_client
pip install .
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
from nordpool import NordpoolClient

# Instantiate the client
client = NordpoolClient()

# Retrieve N2EX day-ahead prices for United Kingdom (UK) and Norway (NO2)
prices = client.get_day_ahead_prices(query_date="2025-03-02",
                                     market="N2EX_DayAhead",
                                     delivery_areas=["NO2", "UK"],
                                     currency="EUR")

print(prices)
```

## API Methods

The `NordpoolClient` class provides several methods to access data endpoints. Some key methods include:

### Auction Data:

This data is very important for guiding which combinations of markets, delivery areas and currencies can be requested from the api.

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