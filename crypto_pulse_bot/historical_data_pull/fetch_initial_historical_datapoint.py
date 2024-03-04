import requests
import psycopg2
import json
from datetime import datetime, timedelta


def fetch_data_from_api(symbol, date):
    url = f"https://api.pro.coinbase.com/products/{symbol}-USD/candles?start={date}&end={date}&granularity=86400"
    response = requests.get(url)
    return response.json()

def insert_data_into_database(symbol, data, cursor):
    for entry in data:
        unix_timestamp, low, high, open, close, volume = entry
        entry_date = datetime.fromtimestamp(unix_timestamp)
        insert_query = """
        INSERT INTO crypto_prices (symbol, unix_timestamp, entry_date, open_price, high_price, low_price, close_price, volume, created_at, updated_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW())
        """
        cursor.execute(insert_query, (symbol, unix_timestamp, entry_date, open, high, low, close, volume))

def main():
    symbols_path = 'config/db_params_password.json'
    with open(symbols_path, 'r') as file:
        data = json.load(file)
        password = data['password']

    db_params = {
        'database': 'crypto_prices_db',
        'user': 'davidkassin',
        'password': password,
        'host': 'localhost',
        'port': 5432
    }

    coin_symbols = ["BTC", "1INCH", "AAVE", "ADA", "ALGO", "ANKR", "ATOM", "AVAX", "AXS", "BAL", "BAND", "BAT", "BCH", "BNT", "BTRST", "CRV", "CTSI", "DASH", "DOGE", "DOT", "ENJ", "EOS", "ETC", "ETH", "FIL", "FORTH", "GRT", "ICP", "KNC", "LINK", "LRC", "LTC", "MANA", "MATIC", "MKR", "NKN", "NMR", "OGN", "ORN", "RAD", "REQ", "RLC", "SKL", "SNX", "SOL", "STORJ", "SUSHI", "TRB", "TRU", "UMA", "UNI", "WBTC", "WCFG", "XLM", "XTZ", "YFI", "ZEC", "ZEN"]

    date = (datetime.now() - timedelta(days=500)).date()

    try:
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()

        for symbol in coin_symbols:
            data = fetch_data_from_api(symbol, date)
            if data:
                insert_data_into_database(symbol, data, cursor)

        conn.commit()
        cursor.close()
        conn.close()
        print("Historical data inserted successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()