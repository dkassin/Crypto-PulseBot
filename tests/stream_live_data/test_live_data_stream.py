import pytest
from unittest.mock import MagicMock
import json
from crypto_pulse_bot.stream_live_data.live_data_stream import LivePriceUpdater

def test_get_existing_tickers():
    live_price_updater = LivePriceUpdater()
    live_price_updater.get_existing_tickers()

    assert len(live_price_updater.tickers_cache) == 60

def test_on_open():
    live_price_updater = LivePriceUpdater()
    mock_ws = MagicMock()
    live_price_updater.on_open(mock_ws)
    mock_ws.send.assert_called_once_with(json.dumps(live_price_updater.subscribe_message))

def test_on_message():
    live_price_updater = LivePriceUpdater()
    mock_ws = MagicMock()
    sample_message = {
        'type': 'ticker',
        'product_id': 'BTC-USD',
        'price': '50000'
    }

    live_price_updater.on_message(mock_ws, json.dumps(sample_message))
    assert live_price_updater.latest_prices == {'BTC-USD': '50000'}