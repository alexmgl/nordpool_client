from nordpool import NordpoolClient
import json
import pprint

if __name__ == '__main__':

    client = NordpoolClient()
    client.get_auction_data_availability(save=True)
    client.get_auction_data_availability_latest(save=True)

    prices = client.get_day_ahead_prices(query_date="2025-03-02",
                                         market="N2EX_DayAhead",
                                         delivery_areas=["NO2"],
                                         currency="EUR")

    print(prices)
