import requests
from datetime import date
from typing import Optional, Dict, List, Set, Union, Any
import datetime
import json
import os

class NordpoolClient:

    """
    A client for interacting with the Nordpool Data Portal API.
    Provides methods to retrieve various types of electricity market data.
    """

    # Base configuration
    BASE_URL = "https://dataportal-api.nordpoolgroup.com/api"

    def __init__(self, session: Optional[requests.Session] = None):
        """
        Initialise the Nordpool client.

        Args:
            session: Optional requests.Session object. If not provided, a new session will be created.
        """

        self.session = session or requests.Session()

        self.auction_config = self.get_auction_data_availability()
        self._update_market_config()

        self.D = datetime.date.today().strftime("%Y-%m-%d")

        self.script_dir = os.path.dirname(os.path.abspath(__file__))

    def _make_request(self, endpoint: str, params: Dict[str, Any]) -> Dict:
        """
        Make a GET request to the API.

        Args:
            endpoint: API endpoint to call
            params: Query parameters

        Returns:
            JSON response as dictionary
        """
        url = f"{self.BASE_URL}/{endpoint}"
        response = self.session.get(url, params=params)
        response.raise_for_status()  # Raise exception for non-200 responses
        return response.json()

    # Auction Data
    def get_auction_data_availability(self, save=False, **kwargs):
        """
        Get the latest available auction data.

        Args:
            save (bool): If True, save the response to a JSON file.
            **kwargs: Additional parameters to pass to the API

        Returns:
            dict: Latest auction config.
        """
        endpoint = "AuctionDataAvailability"
        params = {}
        params.update(kwargs)

        json_response = self._make_request(endpoint, params)

        if save:
            # Get the directory where this script is located

            # Create a full path for the output file relative to the script directory
            output_file = os.path.join(self.script_dir, "AuctionDataAvailability.json")
            with open(output_file, "w") as f:
                json.dump(json_response, f, indent=4)
            print(f"Data saved to {output_file}")

        return json_response

    def get_auction_data_availability_latest(self, save=False, **kwargs) -> Dict:
        """
        Get the latest available auction data.

        Args:
            save (bool): If True, save the response to a JSON file.
            **kwargs: Additional parameters to pass to the API

        Returns:
            dict: Latest auction data availability.
        """
        endpoint = "AuctionDataAvailability/GetLatest"
        params = {}
        params.update(kwargs)

        json_response = self._make_request(endpoint, params)

        if save:
            # Create a full path for the output file relative to the script directory
            output_file = os.path.join(self.script_dir, "AuctionDataAvailabilityLatest.json")
            with open(output_file, "w") as f:
                json.dump(json_response, f, indent=4)
            print(f"Data saved to {output_file}")

        return json_response

    def get_day_ahead_prices(self, query_date: Union[str, date], delivery_areas: List[str],
                             currency: str = "EUR", market: str = "DayAhead", **kwargs) -> Dict:
        """
        Get day ahead prices for multiple areas.

        Args:
            query_date: Date for which to retrieve data (YYYY-MM-DD)
            delivery_areas: List of delivery areas
            currency: Currency code
            market: Market code
            **kwargs: Additional parameters to pass to the API

        Returns:
            Day ahead prices data
        """
        if isinstance(query_date, date):
            query_date = query_date.isoformat()

        endpoint = "DayAheadPrices"
        params = {
            "date": query_date,
            "market": market,
            "deliveryArea": ",".join(delivery_areas),
            "currency": currency
        }
        params.update(kwargs)
        return self._make_request(endpoint, params)

    def get_single_area_price_history(self, query_date: Union[str, date], delivery_area: str,
                                      currency: str = "EUR", market: str = "DayAhead", **kwargs) -> Dict:
        """
        Get price history for a single delivery area.

        Args:
            query_date: Date for which to retrieve data (YYYY-MM-DD)
            delivery_area: Delivery area code
            currency: Currency code
            market: Market code
            **kwargs: Additional parameters to pass to the API

        Returns:
            Price history data for the specified area
        """
        if isinstance(query_date, date):
            query_date = query_date.isoformat()

        endpoint = "DayAheadPrices/singleAreaHistory"
        params = {
            "date": query_date,
            "market": market,
            "deliveryArea": delivery_area,
            "currency": currency
        }
        params.update(kwargs)
        return self._make_request(endpoint, params)

    def get_aggregate_prices(self, year: int, delivery_areas: List[str],
                             currency: str = "EUR", market: str = "DayAhead", **kwargs) -> Dict:
        """
        Get aggregated prices for a year.

        Args:
            year: Year for which to retrieve data
            delivery_areas: List of delivery areas
            currency: Currency code
            market: Market code
            **kwargs: Additional parameters to pass to the API

        Returns:
            Aggregated price data
        """
        endpoint = "AggregatePrices"
        params = {
            "year": year,
            "market": market,
            "deliveryArea": ",".join(delivery_areas),
            "currency": currency
        }
        params.update(kwargs)
        return self._make_request(endpoint, params)

    def get_annual_aggregate_prices(self, delivery_areas: List[str],
                                    currency: str = "EUR", market: str = "DayAhead", **kwargs) -> Dict:
        """
        Get annual aggregated prices.

        Args:
            delivery_areas: List of delivery areas
            currency: Currency code
            market: Market code
            **kwargs: Additional parameters to pass to the API

        Returns:
            Annual aggregated price data
        """
        endpoint = "AggregatePrices/GetAnnuals"
        params = {
            "market": market,
            "deliveryArea": ",".join(delivery_areas),
            "currency": currency
        }
        params.update(kwargs)
        return self._make_request(endpoint, params)

    def get_system_price(self, query_date: Union[str, date], currency: str = "EUR", **kwargs) -> Dict:
        """
        Get system price data.

        Args:
            query_date: Date for which to retrieve data (YYYY-MM-DD)
            currency: Currency code
            **kwargs: Additional parameters to pass to the API

        Returns:
            System price data
        """
        if isinstance(query_date, date):
            query_date = query_date.isoformat()

        endpoint = "DayAheadSystem"
        params = {
            "date": query_date,
            "currency": currency
        }
        params.update(kwargs)
        return self._make_request(endpoint, params)

    def get_day_ahead_volumes(self, query_date: Union[str, date], delivery_areas: List[str],
                              market: str = "DayAhead", **kwargs) -> Dict:
        """
        Get day ahead volumes for multiple areas.

        Args:
            query_date: Date for which to retrieve data (YYYY-MM-DD)
            delivery_areas: List of delivery areas
            market: Market code
            **kwargs: Additional parameters to pass to the API

        Returns:
            Day ahead volumes data
        """
        if isinstance(query_date, date):
            query_date = query_date.isoformat()

        endpoint = "DayAheadVolumes/multiple"
        params = {
            "date": query_date,
            "market": market,
            "deliveryAreas": ",".join(delivery_areas)
        }
        params.update(kwargs)
        return self._make_request(endpoint, params)

    def get_day_ahead_capacities(self, query_date: Union[str, date], delivery_area: str,
                                 market: str = "DayAhead", **kwargs) -> Dict:
        """
        Get day ahead capacities for a delivery area.

        Args:
            query_date: Date for which to retrieve data (YYYY-MM-DD)
            delivery_area: Delivery area code
            market: Market code
            **kwargs: Additional parameters to pass to the API

        Returns:
            Day ahead capacities data
        """
        if isinstance(query_date, date):
            query_date = query_date.isoformat()

        endpoint = "DayAheadCapacities"
        params = {
            "date": query_date,
            "market": market,
            "deliveryArea": delivery_area
        }
        params.update(kwargs)
        return self._make_request(endpoint, params)

    def get_day_ahead_flow(self, query_date: Union[str, date], delivery_area: str,
                           market: str = "DayAhead", **kwargs) -> Dict:
        """
        Get day ahead flow for a delivery area.

        Args:
            query_date: Date for which to retrieve data (YYYY-MM-DD)
            delivery_area: Delivery area code
            market: Market code
            **kwargs: Additional parameters to pass to the API

        Returns:
            Day ahead flow data
        """
        if isinstance(query_date, date):
            query_date = query_date.isoformat()

        endpoint = "DayAheadFlow"
        params = {
            "date": query_date,
            "market": market,
            "deliveryArea": delivery_area
        }
        params.update(kwargs)
        return self._make_request(endpoint, params)

    def get_aggregated_bid_curves(self, query_date: Union[str, date], market_code: str,
                                  cluster_name: str, **kwargs) -> Dict:
        """
        Get aggregated bidding curves.

        Args:
            query_date: Date for which to retrieve data (YYYY-MM-DD)
            market_code: Market code (e.g., NPSDA, IDA2)
            cluster_name: Cluster name (e.g., BALTIC, NO)
            **kwargs: Additional parameters to pass to the API

        Returns:
            Aggregated bidding curves data
        """
        if isinstance(query_date, date):
            query_date = query_date.isoformat()

        endpoint = "AggregatedBidCurves"
        params = {
            "date": query_date,
            "marketCode": market_code,
            "clusterName": cluster_name
        }
        params.update(kwargs)
        return self._make_request(endpoint, params)

    def get_scheduled_physical_flows(self, query_date: Union[str, date], delivery_area: str,
                                     market: str = "DayAhead", **kwargs) -> Dict:
        """
        Get scheduled physical flows for a delivery area.

        Args:
            query_date: Date for which to retrieve data (YYYY-MM-DD)
            delivery_area: Delivery area code
            market: Market code
            **kwargs: Additional parameters to pass to the API

        Returns:
            Scheduled physical flows data
        """
        if isinstance(query_date, date):
            query_date = query_date.isoformat()

        endpoint = "DayAheadFlow/scheduledPhysicalFlows"
        params = {
            "date": query_date,
            "market": market,
            "deliveryArea": delivery_area
        }
        params.update(kwargs)
        return self._make_request(endpoint, params)

    def get_flow_based_constraints(self, query_date: Union[str, date], flow_based_domain: str,
                                   market: str = "DayAhead", **kwargs) -> Dict:
        """
        Get flow-based constraints.

        Args:
            query_date: Date for which to retrieve data (YYYY-MM-DD)
            flow_based_domain: Flow-based domain code
            market: Market code
            **kwargs: Additional parameters to pass to the API

        Returns:
            Flow-based constraints data
        """
        if isinstance(query_date, date):
            query_date = query_date.isoformat()

        endpoint = "AuctionFlowConstraints"
        params = {
            "date": query_date,
            "market": market,
            "flowBasedDomain": flow_based_domain
        }
        params.update(kwargs)
        return self._make_request(endpoint, params)

    # EPAD data

    def get_epad_results(self, query_date: Union[str, date], **kwargs) -> Dict:
        """
        Get EPAD auction results.

        Args:
            query_date: Date for which to retrieve data (YYYY-MM-DD)
            **kwargs: Additional parameters to pass to the API

        Returns:
            EPAD auction results
        """
        if isinstance(query_date, date):
            query_date = query_date.isoformat()

        endpoint = f"EpadData/results/{query_date}"
        params = {}
        params.update(kwargs)
        return self._make_request(endpoint, params)

    def get_epad_yearly_results(self, year: int, **kwargs) -> Dict:
        """
        Get yearly EPAD results.

        Args:
            year: Year for which to retrieve data
            **kwargs: Additional parameters to pass to the API

        Returns:
            Yearly EPAD results
        """
        endpoint = f"EpadData/years/results/{year}"
        params = {}
        params.update(kwargs)
        return self._make_request(endpoint, params)

    def get_epad_bid_curves(self, query_date: Union[str, date], **kwargs) -> Dict:
        """
        Get EPAD bid curves.

        Args:
            query_date: Date for which to retrieve data (YYYY-MM-DD)
            **kwargs: Additional parameters to pass to the API

        Returns:
            EPAD bid curves
        """
        if isinstance(query_date, date):
            query_date = query_date.isoformat()

        endpoint = f"EpadData/bid-curves/{query_date}"
        params = {}
        params.update(kwargs)
        return self._make_request(endpoint, params)

    def get_epad_yearly_bid_curves(self, year: int, **kwargs) -> Dict:
        """
        Get yearly EPAD bid curves.

        Args:
            year: Year for which to retrieve data
            **kwargs: Additional parameters to pass to the API

        Returns:
            Yearly EPAD bid curves
        """
        endpoint = f"EpadData/years/bid-curve/{year}"
        params = {}
        params.update(kwargs)
        return self._make_request(endpoint, params)

    # Intraday market

    def get_intraday_market_statistics(self, query_date: Union[str, date], delivery_area: str, **kwargs) -> Dict:
        """
        Get intraday market statistics.

        Args:
            query_date: Date for which to retrieve data (YYYY-MM-DD)
            delivery_area: Delivery area code
            **kwargs: Additional parameters to pass to the API

        Returns:
            Intraday market statistics
        """
        if isinstance(query_date, date):
            query_date = query_date.isoformat()

        endpoint = "IntradayMarketStatistics"
        params = {
            "date": query_date,
            "deliveryArea": delivery_area
        }
        params.update(kwargs)
        return self._make_request(endpoint, params)

    def get_intraday_hourly_statistics(self, query_date: Union[str, date], delivery_area: str, **kwargs) -> Dict:
        """
        Get hourly intraday market statistics.

        Args:
            query_date: Date for which to retrieve data (YYYY-MM-DD)
            delivery_area: Delivery area code
            **kwargs: Additional parameters to pass to the API

        Returns:
            Hourly intraday market statistics
        """
        if isinstance(query_date, date):
            query_date = query_date.isoformat()

        endpoint = "IntradayMarketStatistics/hourly"
        params = {
            "date": query_date,
            "deliveryArea": delivery_area
        }
        params.update(kwargs)
        return self._make_request(endpoint, params)

    # Power system data

    def get_manual_frequency_restoration_reserve(self, query_date: Union[str, date],
                                                 delivery_areas: List[str], **kwargs) -> Dict:
        """
        Get manual frequency restoration reserve (mFRR) data.

        Args:
            query_date: Date for which to retrieve data (YYYY-MM-DD)
            delivery_areas: List of delivery areas
            **kwargs: Additional parameters to pass to the API

        Returns:
            mFRR data
        """
        if isinstance(query_date, date):
            query_date = query_date.isoformat()

        endpoint = "ManualFrequencyRestorationReserve/multiple"
        params = {
            "date": query_date,
            "deliveryAreas": ",".join(delivery_areas)
        }
        params.update(kwargs)
        return self._make_request(endpoint, params)

    def get_consumption(self, query_date: Union[str, date], delivery_areas: List[str],
                        locations: List[str] = None, **kwargs) -> Dict:
        """
        Get consumption data.

        Args:
            query_date: Date for which to retrieve data (YYYY-MM-DD)
            delivery_areas: List of delivery areas
            locations: Optional list of specific locations
            **kwargs: Additional parameters to pass to the API

        Returns:
            Consumption data
        """
        if isinstance(query_date, date):
            query_date = query_date.isoformat()

        endpoint = "Consumption"
        params = {
            "date": query_date,
            "deliveryAreas": ",".join(delivery_areas),
            "locations": ",".join(locations) if locations else ""
        }
        params.update(kwargs)
        return self._make_request(endpoint, params)

    def get_consumption_forecast(self, query_date: Union[str, date], delivery_areas: List[str],
                                 locations: List[str] = None, **kwargs) -> Dict:
        """
        Get consumption forecast data.

        Args:
            query_date: Date for which to retrieve data (YYYY-MM-DD)
            delivery_areas: List of delivery areas
            locations: Optional list of specific locations
            **kwargs: Additional parameters to pass to the API

        Returns:
            Consumption forecast data
        """
        if isinstance(query_date, date):
            query_date = query_date.isoformat()

        endpoint = "ConsumptionPrognoses"
        params = {
            "date": query_date,
            "deliveryAreas": ",".join(delivery_areas),
            "locations": ",".join(locations) if locations else ""
        }
        params.update(kwargs)
        return self._make_request(endpoint, params)

    def get_production(self, query_date: Union[str, date], delivery_area: str,
                       location: str = "", **kwargs) -> Dict:
        """
        Get production data.

        Args:
            query_date: Date for which to retrieve data (YYYY-MM-DD)
            delivery_area: Delivery area code
            location: Optional specific location
            **kwargs: Additional parameters to pass to the API

        Returns:
            Production data
        """
        if isinstance(query_date, date):
            query_date = query_date.isoformat()

        endpoint = "ProductionData"
        params = {
            "date": query_date,
            "deliveryArea": delivery_area,
            "location": location
        }
        params.update(kwargs)
        return self._make_request(endpoint, params)

    def get_physical_flows(self, query_date: Union[str, date], delivery_area: str, **kwargs) -> Dict:
        """
        Get physical flows data.

        Args:
            query_date: Date for which to retrieve data (YYYY-MM-DD)
            delivery_area: Delivery area code
            **kwargs: Additional parameters to pass to the API

        Returns:
            Physical flows data
        """
        if isinstance(query_date, date):
            query_date = query_date.isoformat()

        endpoint = "PhysicalFlows"
        params = {
            "date": query_date,
            "deliveryArea": delivery_area
        }
        params.update(kwargs)
        return self._make_request(endpoint, params)

    def _update_market_config(self):

        # Prepare a dictionary to store the extracted information
        self.markets_info = {}

        for market in self.auction_config:
            market_key = market.get("market", "Unknown")
            display_name = market.get("marketDisplayName", "")

            self.markets_info[market_key] = display_name

        return self.markets_info


if __name__ == '__main__':
    pass
