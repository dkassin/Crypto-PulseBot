# Crypto-PulseBot

## Description

Crypto-PulseBot is a backend application designed to empower crypto traders with real-time data and analytical capabilities. Leveraging Python and PostgreSQL, the application streams live cryptocurrency prices directly into Google Sheets via API and stores historical data for deep algorithmic trading analysis.

Features:
- Live Price Streaming: Just like a Bloomberg terminal, Crypto-PulseBot offers real-time streaming of cryptocurrency prices using websockets, allowing users to monitor the market as it changes.
- Integration with Google Sheets: Stream live data directly into Google Sheets, enabling easy access and manipulation of data for trading strategies and decision-making.
- Historical Data Mining: Utilizes a PostgreSQL database to store and mine historical trading data, essential for backtesting trading strategies and performing comprehensive market analyses.
- Concurrency, with the ability to set up live prices with multiple exchanges at once. (You may need to change update frequency to 4-5 seconds to not run into rate limits)   

## Requirements and Setup (for Mac):

### Python
- Python 3.9.12

### Database
- PostgreSQL

### Schema
- We use a single table schema to just load prices, this is only used for the data miner, this can be skipped if you're only interested in the websocket data streaming.

[![schema_screenshot](https://i.postimg.cc/Pqg5khpG/Screenshot-2024-06-03-at-8-52-26-AM.png)](https://postimg.cc/wtkphCQF)

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

[![screen_shot_db_params](https://i.postimg.cc/K8YzP0SW/Screenshot-2024-06-03-at-10-16-40-AM.png)](https://postimg.cc/mt0BRNr3)

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

[![screenshot_spreadsheet_id](https://i.postimg.cc/Gp8mN9pJ/Screenshot-2024-06-03-at-9-59-47-AM.png)](https://postimg.cc/gwppLz8n)
  
<br />

**Sample config.json**

[![screenshot_config](https://i.postimg.cc/T3HPCnT3/Screenshot-2024-06-03-at-9-58-17-AM.png)](https://postimg.cc/RWK9063k)

<br />

**Sample google_auth.json**

[![google_auth](https://i.postimg.cc/tTFCqfWs/Screenshot-2024-06-03-at-9-36-28-AM.png)](https://postimg.cc/0M2qZVtv)

**MAKE SURE to add the config files to your .gitignore (THIS IS IMPORTANTE)**  

If you do not already have a .gitignore file, create a file in called .gitignore and add google_auth.json and config.json to it.

**This should complete basic setup**

**The google sheet is very senstive to naming conventions, make sure of the following**

-  This utilizes the coinbase API, all coin tickers should be in the column A in the google sheet.
-  The sheet name in the bottom left should be Prices. 
-  The coin symbols in the google sheet should be in the format ETH-USD, the live price should populate in the B column.


# Happy Hunting!!

     
