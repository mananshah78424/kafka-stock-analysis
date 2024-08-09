import time
from datetime import datetime
from pprint import pprint

import requests
import schedule


def fetch_data():
    today_date = datetime.now().strftime('%Y-%m-%d')
    print(f"Fetching data for: {today_date} at {datetime.now().time()}")
    
    # Replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=15min&apikey=B15MM91DDRIHMJA6&adjusted=false&extended_hours=false'
    r = requests.get(url)
    data = r.json()
    time_series = data.get("Time Series (15min)", {})
    
    if time_series:
        latest_time = max(time_series.keys())  # Get the most recent timestamp
        latest_record = {latest_time: time_series[latest_time]}
        print("Latest record:")
        pprint(latest_record)
    else:
        print("No time series data found for today.")

def wait_until_initial_time(initial_time):
    now = datetime.now()
    if now > initial_time:
        print("Initial time has already passed for today. Exiting...")
        return

    wait_seconds = (initial_time - now).total_seconds()
    print(f"Waiting for {wait_seconds} seconds until the initial run at {initial_time.time()}")

    time.sleep(wait_seconds)
    fetch_data()  # Run once at the start time

def schedule_recurring_task():
    schedule.every(5).minutes.do(fetch_data)
    while True:
        schedule.run_pending()

now = datetime.now()
initial_time = datetime(now.year, now.month, now.day, 9, 33)
if now > initial_time:
    print("Initial time has already passed for today. Please run the script before 9:31 AM.")
else:
    wait_until_initial_time(initial_time)
    schedule_recurring_task()

# # Pretty print the JSON data
# pprint(data)
