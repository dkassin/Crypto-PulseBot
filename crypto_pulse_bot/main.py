from historical_data_pull.fetch_and_insert_data import HistoricalCryptoDataUpdater
from stream_live_data.live_data_stream import LivePriceUpdater

def main():
    data_updater = HistoricalCryptoDataUpdater()
    data_updater.update_crypto_data()

    live_price_updater = LivePriceUpdater()
    live_price_updater.run()

if __name__ == "__main__":
    main()