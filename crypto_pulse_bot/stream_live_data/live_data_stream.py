from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from time import sleep
import websocket, json
import threading
import pdb

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

        symbols_path = 'config/symbols.json'
        with open(symbols_path, 'r') as file:
            data = json.load(file)
            self.product_ids = data['product_ids']

        self.subscribe_message = {
            'type': 'subscribe',
            "channels": [
                "level2",
                "heartbeat",
                {
                    "name": "ticker",
                    "product_ids": self.product_ids
                }
            ]
        }

        self.tickers_cache = {}
        self.latest_prices = {}
        self.get_existing_tickers()

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

    def run(self):
        self.start_update_thread()
        socket = 'wss://ws-feed.pro.coinbase.com'
        ws = websocket.WebSocketApp(socket,on_open=self.on_open, on_message=self.on_message)
        ws.run_forever()

if __name__ == "__main__":
    live_price_updater = LivePriceUpdater()
    live_price_updater.run()