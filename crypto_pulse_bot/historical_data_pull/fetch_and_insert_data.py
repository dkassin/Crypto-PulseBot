import requests
import psycopg2
import json
import pytz
from datetime import datetime, timedelta, timezone


class HistoricalCryptoDataUpdater:
    def __init__(self, symbols_path='config/db_params_password.json'):
        with open(symbols_path, 'r') as file:
            data = json.load(file)
            self.db_params = {
                'database': 'crypto_prices_db',
                'user': 'davidkassin',
                'password': data['password'],
                'host': 'localhost',
                'port': 5432
            }
        self.granularity = 3600
        self.coin_symbols = [ "BTC", "ETH"]
    
    def connect_to_database(self):
        return psycopg2.connect(**self.db_params)

    def get_current_time_with_dst(self, timezone_str):
        tz = pytz.timezone(timezone_str)
        return datetime.now(tz)


    def get_last_timestamp(self, symbol, cursor):
        try:
            cursor.execute("SELECT max(unix_timestamp) FROM crypto_prices WHERE symbol = %s", (symbol,))
            result = cursor.fetchone()
            if result[0]:
                return datetime.fromtimestamp(result[0], tz=timezone.utc)
            else:
                return datetime.now(timezone.utc) - timedelta(days=75)
        except Exception as e:
            print(f"Error fetching last timestamp for {symbol}: {e}")
            return datetime.now(timezone.utc) - timedelta(days=75)

    def fetch_data_in_batches(self, symbol, start_time, cursor):
        batch_interval = timedelta(hours=299)
        current_time = self.get_current_time_with_dst('America/Denver')
        
        while start_time < current_time:
            batch_end_time = min(start_time + batch_interval, current_time)
            
            start_time_str = start_time.isoformat()
            batch_end_time_str = batch_end_time.isoformat()

            url = f"https://api.pro.coinbase.com/products/{symbol}-USD/candles?granularity={self.granularity}&start={start_time_str}&end={batch_end_time_str}"
            response = requests.get(url)
            data = response.json()

            if data:
                for entry in data:
                    try:
                        unix_timestamp, low, high, open, close, volume = entry
                        entry_date = datetime.fromtimestamp(unix_timestamp)

                        insert_query = """
                        INSERT INTO crypto_prices (symbol, unix_timestamp, entry_date, open_price, high_price, low_price, close_price, volume, created_at, updated_at)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW())
                        """
                        cursor.execute(insert_query, (symbol, unix_timestamp, entry_date, open, high, low, close, volume))
                    except Exception as e:
                        print(f"Error inserting data for {symbol}: {e}")
                print(f"Successfully inserted data for {symbol} up to {batch_end_time}.")
            else:
                print(f"No data fetched for {symbol} between {start_time} and {batch_end_time}")

            start_time = batch_end_time

    def update_crypto_data(self):
        try:
            conn = self.connect_to_database()
            cursor = conn.cursor()

            for symbol in self.coin_symbols:
                try:
                    last_timestamp = self.get_last_timestamp(symbol, cursor)
                    self.fetch_data_in_batches(symbol, last_timestamp, cursor)
                except Exception as e:
                    print(f"Error processing {symbol}: {e}")

            conn.commit()
            cursor.close()
            conn.close()        

            print("Hourly data update process completed.")
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    HistoricalPriceUpdater = HistoricalCryptoDataUpdater()
    HistoricalPriceUpdater.update_crypto_data()