import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
import pytz
import requests
from crypto_pulse_bot.historical_data_pull.fetch_initial_historical_datapoint import (
    fetch_data_from_api,
    insert_data_into_database,
    main
)

def test_fetch_data_from_api_success():
    date = datetime(2023, 1, 1).date()
    mock_response = [{"data": "example"}]
    with patch('crypto_bot.historical_data_pull.fetch_initial_historical_datapoint.requests.get') as mock_get:
        mock_get.return_value.json.return_value = mock_response
        data = fetch_data_from_api('BTC', date)
    
    assert data == mock_response

def test_fetch_data_from_api_empty_response():
    date = datetime(2023, 1, 1).date()

    with patch('crypto_bot.historical_data_pull.fetch_initial_historical_datapoint.requests.get') as mock_get:
        mock_get.return_value.json.return_value = []
        data = fetch_data_from_api('BTC', date)
    
    assert data == []

def test_insert_data_into_database():
    mock_data = [(123456789, 100, 200, 150, 180, 500)]
    mock_cursor = MagicMock()

    insert_data_into_database('BTC', mock_data, mock_cursor)
    mock_cursor.execute.assert_called_once()

def test_main():
    test_date = datetime(2023, 1, 1)
    mock_fetch_data = [{"data": "example"}]
    mock_db_connection = MagicMock()
    mock_cursor = MagicMock()

    with patch('crypto_bot.historical_data_pull.fetch_initial_historical_datapoint.fetch_data_from_api', return_value = mock_fetch_data) as mock_fetch:
        with patch('crypto_bot.historical_data_pull.fetch_initial_historical_datapoint.insert_data_into_database') as mock_insert:
            with patch('crypto_bot.historical_data_pull.fetch_initial_historical_datapoint.psycopg2.connect')as mock_connect:
                mock_connect.return_value = mock_db_connection
                mock_db_connection.cursor.return_value= mock_cursor
                with patch('crypto_bot.historical_data_pull.fetch_initial_historical_datapoint.datetime') as mock_datetime:
                    mock_datetime.now.return_value = test_date
                    date = (mock_datetime.now.return_value - timedelta(days=500)).date()

                    main()
    
    assert mock_fetch.call_count == 58
    mock_connect.assert_called_once()
    mock_db_connection.commit.assert_called_once()
    assert mock_insert.call_count == 58
    mock_cursor.close.assert_called_once()
    mock_db_connection.close.assert_called_once()