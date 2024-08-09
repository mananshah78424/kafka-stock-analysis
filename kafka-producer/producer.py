import datetime
import time
from datetime import datetime, timedelta

import pytz
import requests
import schedule
from bs4 import BeautifulSoup


def web_content_div(web_content, test_id):
    element = web_content.find('fin-streamer', {'data-testid': test_id})
    if element:
        span = element.find('span')
        if span:
            return span.get_text()
    return None

def real_time_price(stock_code):
    url = f"https://finance.yahoo.com/quote/{stock_code}/"
    headers = {
        'Cache-Control': 'no-cache',
        'Pragma': 'no-cache',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        r = requests.get(url, headers=headers)
        web_content = BeautifulSoup(r.text, 'lxml')
        price = web_content_div(web_content, 'qsp-price')
        change = web_content_div(web_content, 'qsp-price-change')
        return price, change
    except Exception as e:
        print(f"An error occurred: {e}")
        return None, None

def is_market_open():
    est = pytz.timezone('US/Eastern')
    current_time = datetime.now(est)
    current_day = current_time.weekday()  # Monday is 0 and Sunday is 6
    market_open_time = current_time.replace(hour=9, minute=30, second=0, microsecond=0)
    market_close_time = current_time.replace(hour=15, minute=30, second=0, microsecond=0)

    if current_day < 5:  # 0-4 corresponds to Monday to Friday
        if market_open_time <= current_time <= market_close_time:
            return True
    return False
est = pytz.timezone('US/Eastern')

def schedule_next_market_open():
    est = pytz.timezone('US/Eastern')
    now = datetime.now(est)
    next_market_open = now.replace(hour=9, minute=30, second=0, microsecond=0)
    if now >= next_market_open:
        next_market_open += timedelta(days=1)
    schedule_time = next_market_open.strftime("%Y-%m-%d %H:%M:%S")
    print(f"Scheduling next market open check at: {schedule_time}")
    schedule.every().day.at("09:30").do(main)

def display_data():
    if is_market_open():
        price, change = real_time_price('BRK-B')
        now = datetime.now(est)

        print(f"Price: {price}, Change: {change}, Time: {now}")
    else:
        print("Market has closed")
        schedule.clear()
def main():
    while is_market_open():
        display_data()
        time.sleep(10)
    schedule_next_market_open()

if __name__ == "__main__":
    main()
    while True:
        schedule.run_pending()
        time.sleep(1)
