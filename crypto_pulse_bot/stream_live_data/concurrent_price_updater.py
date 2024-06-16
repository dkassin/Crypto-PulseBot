import threading
import logging

from .kraken_data_stream import KrakenLivePriceUpdater
from .live_data_stream import LivePriceUpdater

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ConcurrentPriceUpdater:
    def __init__(self) -> None:
        logging.info('Initializing ConcurrentPriceUpdater')

    def start(self):
        logging.info('Starting updaters...')

        coinbase_updater = LivePriceUpdater()
        kraken_updater = KrakenLivePriceUpdater()

        threads = [
            threading.Thread(target= coinbase_updater.run, name="CoinbaseUpdaterThread"),
            threading.Thread(target= kraken_updater.run, name="KrakenUpdaterThread")
        ]

        for thread in threads:
            logging.info(f'Starting thread {thread.name}')
            thread.start()

        for thread in threads:
            thread.join()

if __name__ == "__main__":
    try:
        logging.info('Starting ConcurrentPriceUpdater')
        concurrent_updater = ConcurrentPriceUpdater()
        concurrent_updater.start()
    except Exception as e:
        logging.error(f'An error occurred: {e}')
