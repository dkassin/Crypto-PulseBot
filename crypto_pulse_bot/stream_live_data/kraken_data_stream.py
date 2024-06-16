from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import datetime
from IPython import embed
from time import sleep
import websocket, json
import threading
import pdb

class KrakenLivePriceUpdater:
    def __init__(self):
        SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
        SERVICE_ACCOUNT_FILE = 'config/google_auth.json'
        credentials = Credentials.from_service_account_file(
                SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        self.service = build('sheets', 'v4', credentials=credentials)

        config_path = 'config/config.json'
        with open(config_path, 'r') as config_file:
            config = json.load(config_file)
            self.SPREADSHEET_ID = config['SPREADSHEET_ID_2']

        self.sub_message = {
            "event": "subscribe",
            "pair": ["USDT/EUR", "USDC/EUR", "USDT/GBP", "USDC/GBP", "USDT/AUD", "USDC/AUD", "USDT/CAD", "USDC/CAD","USDT/CHF", "USDC/CHF" ],
            "subscription": {"name": "ticker"}
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
        ws.send(json.dumps(self.sub_message))

    def handle_data(self, pair, data_dict):
        bid = data_dict.get('b',[None])[0]
        ask = data_dict.get('a',[None])[0]
        last_price = data_dict.get('c', [None])[0]

        if pair:
            if pair not in self.latest_prices:
                self.latest_prices[pair] = {}

            if bid:
                self.latest_prices[pair]['bid'] = bid
            if ask:
                self.latest_prices[pair]['ask'] = ask
            if last_price:
                self.latest_prices[pair]['last_price'] = last_price
            print(f"Updated {pair} - Bid: {bid}, Ask: {ask}, Last Trade: {last_price}")

    def on_message(self, ws, message):
        try:
            data = json.loads(message)
            if isinstance(data, list) and len(data) >= 2:
                pair = data[-1]
                data_dict = data[1]
                self.handle_data(pair, data_dict)

        except json.JSONDecodeError as e:
            print("Error decoding JSON:", e)
        except Exception as e:
            print("Error handling message:", e)
                
    def on_error(self, ws, error):
        print("Error:")
        print(error)

    def on_close(self, ws, close_status_code, close_msg):
        print("### closed ###")
        print("Close status code:", close_status_code)
        print("Close message:", close_msg)

    def update_google_sheet(self):
        while True:
            sleep(5)
            if not self.latest_prices:
                continue

            values = []
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            for pair, data in self.latest_prices.items():
                bid = data.get('bid', 'N/A')
                ask = data.get('ask', 'N/A')
                last_price = data.get('last_price', 'N/A')

                row_number = self.tickers_cache.get(pair, None)
                if row_number:
                    bid_range = f'Prices!B{row_number}'
                    ask_range = f'Prices!C{row_number}'
                    last_price_range = f'Prices!D{row_number}'
                    timestamp_range = f'Prices!E{row_number}'
                    
                    values.append({'range': bid_range, 'values': [[bid]]})
                    values.append({'range': ask_range, 'values': [[ask]]})
                    values.append({'range': last_price_range, 'values': [[last_price]]})
                    values.append({'range': timestamp_range, 'values': [[timestamp]]})

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
        ws_url = "wss://ws.kraken.com/"
        ws = websocket.WebSocketApp(ws_url,
                                on_message= self.on_message,
                                on_error= self.on_error,
                                on_close= self.on_close)
        ws.on_open = self.on_open
        ws.run_forever()

if __name__ == "__main__":
    live_price = KrakenLivePriceUpdater()
    live_price.run()

