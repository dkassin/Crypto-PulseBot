# Crypto-PulseBot

## Description

Crypto-PulseBot is a backend application designed to empower crypto traders with real-time data and analytical capabilities. Leveraging Python and PostgreSQL, the application streams live cryptocurrency prices directly into Google Sheets via API and stores historical data for deep algorithmic trading analysis.

Features:
- Live Price Streaming: Just like a Bloomberg terminal, Crypto-PulseBot offers real-time streaming of cryptocurrency prices using websockets, allowing users to monitor the market as it changes.
- Integration with Google Sheets: Stream live data directly into Google Sheets, enabling easy access and manipulation of data for trading strategies and decision-making.
- Historical Data Mining: Utilizes a PostgreSQL database to store and mine historical trading data, essential for backtesting trading strategies and performing comprehensive market analyses.

## Requirements and Setup (for Mac):

### Python
- Python 3.9.12

### Database
- PostgreSQL

### Schema
- We use a single table schema to just load prices, this is only used for the data miner, this can be skipped if you're only interested in the websocket data streaming.

![schema_screenshot](https://private-user-images.githubusercontent.com/76177498/336121500-ee55b9fe-f0f2-49d5-a6ce-5a3e7f71b1bb.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MTc0MjY4MDgsIm5iZiI6MTcxNzQyNjUwOCwicGF0aCI6Ii83NjE3NzQ5OC8zMzYxMjE1MDAtZWU1NWI5ZmUtZjBmMi00OWQ1LWE2Y2UtNWEzZTdmNzFiMWJiLnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNDA2MDMlMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjQwNjAzVDE0NTUwOFomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPTE4ZjYxYzI5NzM2ODcxNzg5MGNjZWY2MmM3Mjk4MTVkN2E4OTU2MTNiYTFhNWY3ZDkzYWQ0NWRkMDc5MzM0MjQmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0JmFjdG9yX2lkPTAma2V5X2lkPTAmcmVwb19pZD0wIn0.UUo5k3MEngQR-FwDd3BdvD11Z5n7af0niih1dumFIWY)

### Setup
#### 1. Clone this repository:
On your local machine open a terminal session and enter the following commands for SSH or HTTPS to clone the repositiory.

- using ssh key <br>
```shell
$ git clone git@github.com:dkassin/Crypto-PulseBot.git
```

- using https <br>
```shell
$ git clone https://github.com/dkassin/Crypto-PulseBot.git
Once cloned, you'll have a new local copy in the directory you ran the clone command in.

- Change to the project directory:<br>
In terminal, use `$cd` to navigate to the Crypto-PulseBot Application project directory.

```shell
$ cd Crypto-PulseBot
```

#### 2. Set up Python Environment (Optional but Recommended):
To set up and activate a virtual environment
```
python3 -m venv env
source env/bin/activate
```

#### 3. Install Dependencies:
Install all required Python libraries using pip:
```
pip install -r requirements.txt
```

#### 4. Configuring PostgreSQL:
Database Setup:

- Start your PostgreSQL server, usually with pg_ctl -D /usr/local/var/postgres start or using the PostgreSQL service in the macOS System Preferences.
```
psql postgres
CREATE DATABASE crypto_prices_db;
\q
```

- Set up the schema as shown in the provided schema screenshot.

In the code, in the fetch_and_insert_data.py and fetch_initial_historical_datapoint.py -- you will have to change the self.db_params to your database setup. the code that must be changed is the user. 

![screen_shot_db_params](https://private-user-images.githubusercontent.com/76177498/336149621-746d960b-a884-46a2-a8ad-44652a14c859.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MTc0MzE4NDAsIm5iZiI6MTcxNzQzMTU0MCwicGF0aCI6Ii83NjE3NzQ5OC8zMzYxNDk2MjEtNzQ2ZDk2MGItYTg4NC00NmEyLWE4YWQtNDQ2NTJhMTRjODU5LnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNDA2MDMlMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjQwNjAzVDE2MTkwMFomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPWI1ZDNlOGEwN2M2MWIyMzY0YmZmNGI1OWM0ZDEyOTZjNWRhY2NjYTYwNThhZTlhZTA0MWY0ZTZjMWIwYmYzODQmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0JmFjdG9yX2lkPTAma2V5X2lkPTAmcmVwb19pZD0wIn0.hPeLhIf7Rj0wkA0UwuK1QpIBL6ZKsmOkkM1BiMQi294)

#### 5. Config directory setup:

In order to have files hidden from github and for the code to work properly, you must set up a config directory and then have properly named files in that directory. Set up the following files in the config directory:
- config.json
- google_auth.json
- db_params_password.json
-- Save this in the db_params_password.json
  ```
  { "password": "whatever your password is" }
  ```

#### 6. Google Sheets API setup:

- Go to the Google Developers Console
- Create a new project, and enable the Google Sheets API for that project
- Create credentials (API key or OAuth 2.0 Client ID) to authenticate your requests. (This can be a tricky step)
- Download the JSON File contain your credentials and save it in the config directory, as google_auth.json. (If you do not have a config directory, created a directory called config, then put the google_auth.json file in there)
-  Also create another file in the config directory called config.json
- In the google sheet you must also make the address in your client email, an editor in the google sheet. (You can find the sheet in the credentials under client email)
  
<br />

**Where to get SPREADSHEET_ID value**

- Go to the google sheet you will use and you can see the value needed in the URL, it should be in place of the Fake in this image

![screenshot_spreadsheet_id](https://private-user-images.githubusercontent.com/76177498/336145031-0c35e048-f3af-48d0-8d33-5a712b392f98.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MTc0MzA3NzQsIm5iZiI6MTcxNzQzMDQ3NCwicGF0aCI6Ii83NjE3NzQ5OC8zMzYxNDUwMzEtMGMzNWUwNDgtZjNhZi00OGQwLThkMzMtNWE3MTJiMzkyZjk4LnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNDA2MDMlMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjQwNjAzVDE2MDExNFomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPThjZmI5MzQxM2U1NTExNzFjZGMwNjE2MTllMDQ4NzI1NjBhMjM3Mjk5OWI3NzRiYzA0NmZjZWE5YjA5MjAxZWEmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0JmFjdG9yX2lkPTAma2V5X2lkPTAmcmVwb19pZD0wIn0.CexSDMCj-khP_F1R6p8iUQ1Dk0q_oNjQhVD668IBj5w)
  
<br />

**Sample config.json**

![screenshot_config](https://private-user-images.githubusercontent.com/76177498/336144871-113b330e-ecc1-475a-83df-2d0b1739aa8b.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MTc0MzA4NjYsIm5iZiI6MTcxNzQzMDU2NiwicGF0aCI6Ii83NjE3NzQ5OC8zMzYxNDQ4NzEtMTEzYjMzMGUtZWNjMS00NzVhLTgzZGYtMmQwYjE3MzlhYThiLnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNDA2MDMlMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjQwNjAzVDE2MDI0NlomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPTNmZjI1MGU0Yjg0ZGFhZWEyMTZmY2E1ODRhOTlkYjRhMDlmNDhlMTNiMjFhMzcwZjUyYWE2MGYyZjlhMzUwZjUmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0JmFjdG9yX2lkPTAma2V5X2lkPTAmcmVwb19pZD0wIn0.nMDnBlluMreRICozoquKFoFs_OI-ZineDUOGUjKq6cM)

<br />

**Sample google_auth.json**


![screenshot](https://private-user-images.githubusercontent.com/76177498/336137726-042acabf-5dc0-43bd-a916-56524d103852.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MTc0Mjk0ODIsIm5iZiI6MTcxNzQyOTE4MiwicGF0aCI6Ii83NjE3NzQ5OC8zMzYxMzc3MjYtMDQyYWNhYmYtNWRjMC00M2JkLWE5MTYtNTY1MjRkMTAzODUyLnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNDA2MDMlMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjQwNjAzVDE1Mzk0MlomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPThlYTNhYTA1YzkwNmYzYzZhN2NkMjI1NWE5OTk0NjA5ZDUyNzE4YzM2YTBhN2M1MDc5Mzg3OTUyNjFiMDlmYWUmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0JmFjdG9yX2lkPTAma2V5X2lkPTAmcmVwb19pZD0wIn0.XyNOwiLzDrfGWSQCtSVnt64CX0SSzXlTVU0CT2cxICI)

**MAKE SURE to add the config files to your .gitignore (THIS IS IMPORTANTE)**  

If you do not already have a .gitignore file, create a file in called .gitignore and add google_auth.json and config.json to it.

**This should complete basic setup**

**The google sheet is very senstive to naming conventions, make sure of the following**

-  This utilizes the coinbase API, all coin tickers should be in the column A in the google sheet.
-  The sheet name in the bottom left should be Prices. 
-  The coin symbols in the google sheet should be in the format ETH-USD, the live price should populate in the B column.


# Happy Hunting!!

     
