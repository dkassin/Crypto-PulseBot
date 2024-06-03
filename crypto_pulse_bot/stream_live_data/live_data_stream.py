from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from time import sleep
import websocket, json
import threading
import pdb
import time

class LivePriceUpdater:
    def __init__(self):
        SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
        SERVICE_ACCOUNT_FILE = 'config/google_auth.json'
        credentials = Credentials.from_service_account_file(
                SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        self.service = build('sheets', 'v4', credentials=credentials)

        config_path = 'config/config.json'
        with open(config_path, 'r') as config_file:
            config = json.load(config_file)
            self.SPREADSHEET_ID = config['SPREADSHEET_ID']

        symbols = { "product_ids": ["ETH-BTC"] }

        self.subscribe_message = {
            'type': 'subscribe',
            "channels": [
                "level2",
                "heartbeat",
                {
                    "name": "ticker",
                    "product_ids": symbols
                }
            ]
        }

        self.tickers_cache = {}
        self.latest_prices = {}
        self.get_existing_tickers()
        self.retry_delay = 5
        self.stop_thread = threading.Event()

    def start_update_thread(self):
        self.thread = threading.Thread(target=self.update_google_sheet)
        self.thread.start()

    def get_existing_tickers(self):
        range_name = 'Prices!A:A'
        result = self.service.spreadsheets().values().get(spreadsheetId= self.SPREADSHEET_ID,
                                                    range=range_name).execute()
        values = result.get('values', [])

        if not values:
            print('No data found.')
            return {}
        else:
            self.tickers_cache = {value[0]: idx + 1 for idx, value in enumerate(values) if value}

    def on_open(self, ws):
        print ('the socket is opened')  
        ws.send(json.dumps(self.subscribe_message))

    def on_message(self, ws, message):
        current_data = json.loads(message)
        if current_data.get('type') == 'ticker':
            product_id = current_data.get('product_id')
            price = current_data.get('price')
            self.latest_prices[product_id] = price

    def on_error(self, ws, error):
        print(f"Websocket ecountered an error: {error}")
        self.reconnect()

    def on_close(self, ws, close_status_code, close_msg):
        print(f"WebSocket closed with status code {close_status_code}: {close_msg}")
        self.reconnect()

    def reconnect(self):
        print(f"Reconnecting in {self.retry_delay} seconds...")
        time.sleep(self.retry_delay)
        self.start_update_thread()
        self.create_and_run_websocket()

    def update_google_sheet(self):
        while True:
            sleep(2)
            if not self.latest_prices:
                continue

            values = []
            for product_id, price in self.latest_prices.items():
                row_number = self.tickers_cache.get(product_id, None)
                if row_number:
                    range_name = f'Prices!B{row_number}'
                    values.append({
                        'range': range_name,
                        'values': [[price]]
                    })

            if values:
                body = {
                    'valueInputOption': 'RAW',
                    'data': values
                }
                try:
                    result = self.service.spreadsheets().values().batchUpdate(
                        spreadsheetId=self.SPREADSHEET_ID, body=body).execute()
                    print(f"Updated {len(values)} rows")
                except Exception as e:
                    print("Failed to update Google Sheet:", e)

            self.latest_prices = {}

    def create_and_run_websocket(self):
        ws = websocket.WebSocketApp(
            'wss://ws-feed.pro.coinbase.com',
            on_open=self.on_open,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close
            )
        ws.run_forever()

    def run(self):
        self.start_update_thread()
        self.create_and_run_websocket()

if __name__ == "__main__":
    live_price_updater = LivePriceUpdater()
    live_price_updater.run()