from nordpool import NordpoolClient
import json
import pprint

if __name__ == '__main__':

    client = NordpoolClient()
    client.get_auction_data_availability(save=True)
    client.get_auction_data_availability_latest(save=True)
