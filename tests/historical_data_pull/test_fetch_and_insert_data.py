import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
import pytz
import requests
from crypto_bot.historical_data_pull.fetch_and_insert_data import HistoricalCryptoDataUpdater

def test_get_current_tie_with_dst():
    test_timezone = 'America/Denver'
    updater = HistoricalCryptoDataUpdater()
    result = updater.get_current_time_with_dst(test_timezone)
    assert isinstance(result, datetime)
    assert result.tzinfo.zone == test_timezone

def test_get_last_timestamp():
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = (123456789,)
    updater = HistoricalCryptoDataUpdater()
    result = updater.get_last_timestamp('BTC', mock_cursor)
    assert isinstance(result, datetime)

def test_fetch_data_in_batches():
    symbol = 'BTC'
    start_time = datetime(2023, 1, 1, tzinfo=pytz.timezone('America/Denver'))
    current_time = start_time + timedelta(hours=1)
    mock_cursor = MagicMock

    mock_response = MagicMock()
    mock_response.json.return_value = [{"data": "example"}]
    updater = HistoricalCryptoDataUpdater()

    with patch('requests.get', return_value=mock_response) as mock_requests_get:
        with patch.object(updater, 'get_current_time_with_dst') as mock_get_current_time:
            mock_get_current_time.return_value = current_time
            updater.fetch_data_in_batches(symbol, start_time, mock_cursor)
    
    expected_url = f"https://api.pro.coinbase.com/products/{symbol}-USD/candles?granularity=3600&start=2023-01-01T00:00:00-07:00&end=2023-01-01T01:00:00-07:00"
    mock_requests_get.assert_called_once_with(expected_url)

def test_fetch_data_in_bathes_empty_response():
    symbol = 'BTC'
    start_time = datetime(2023, 1, 1, tzinfo=pytz.timezone('America/Denver'))
    current_time = start_time + timedelta(hours=1)
    mock_cursor = MagicMock()

    mock_response = MagicMock()
    mock_response.json.return_value = None
    updater = HistoricalCryptoDataUpdater()

    with patch('requests.get', return_value=mock_response):
        with patch.object(updater, 'get_current_time_with_dst') as mock_get_current_time:
            mock_get_current_time.return_value = current_time
            with patch('builtins.print') as mock_print:
                updater.fetch_data_in_batches(symbol, start_time, mock_cursor)
    
    expected_message = f"No data fetched for {symbol} between {start_time} and {current_time}"
    mock_print.assert_called_once_with(expected_message)

def test_update_crypto_date():
    updater = HistoricalCryptoDataUpdater()
    mock_cursor = MagicMock()
    mock_fetch_data = [{"data": "example"}]

    with patch.object(updater, 'connect_to_database') as mock_connect_to_database:
        mock_connect_to_database.return_value = mock_cursor
        with patch.object(updater, 'get_last_timestamp') as mock_get_last_timestamp:
            mock_get_last_timestamp.return_value = datetime(2023, 1, 1)
            with patch.object(updater, 'fetch_data_in_batches') as mock_fetch_data_in_batches:
                updater.update_crypto_data()
    
    mock_connect_to_database.assert_called_once()
    mock_get_last_timestamp.assert_called()
    mock_fetch_data_in_batches.assert_called()
    mock_cursor.commit.assert_called_once()
    mock_cursor.close.assert_called_once()
    