import datetime
import time
from datetime import datetime, timedelta

from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
from json import dumps

# import psycopg2
import pytz
import requests
import schedule
from bs4 import BeautifulSoup
from kafka import KafkaProducer

broker = "kafka:9092"
topicname = "stockPrice"

# Database connection details
DB_HOST = "localhost"
DB_NAME = "kafka"
DB_USER = "postgres"
DB_PASSWORD = ""  # if no password, leave it empty

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
    market_close_time = current_time.replace(hour=16, minute=0, second=0, microsecond=0)

    if current_day < 5 and market_open_time <= current_time <= market_close_time:
        return True
    return False

def schedule_next_market_open():
    est = pytz.timezone('US/Eastern')
    now = datetime.now(est)
    next_market_open = now.replace(hour=9, minute=30, second=0, microsecond=0)
    if now >= next_market_open:
        next_market_open += timedelta(days=1)
    schedule_time = next_market_open.strftime("%Y-%m-%d %H:%M:%S")
    print(f"Scheduling next market open check at: {schedule_time}")
    schedule.every().day.at("09:30").do(main)

# def insert_data_to_db(timestamp, stock_code, price, change):
#     try:
#         conn = psycopg2.connect(
#             host=DB_HOST,
#             database=DB_NAME,
#             user=DB_USER,
#             password=DB_PASSWORD
#         )
#         cur = conn.cursor()
#         query = """
#         INSERT INTO stock_prices (timestamp, stock_code, price, change)
#         VALUES (%s, %s, %s, %s)
#         """
#         cur.execute(query, (timestamp, stock_code, price, change))
#         conn.commit()
#         print("Logged into database")
#         cur.close()
#         conn.close()
#     except Exception as e:
#         print(f"Database error: {e}")


def display_data(stock_code):
    producer = KafkaProducer(bootstrap_servers=broker, value_serializer=lambda x:dumps(x).encode('utf-8'))
    if is_market_open():
        price, change = real_time_price(stock_code)
        now = datetime.now(pytz.timezone('US/Eastern'))
        if price and change:
            print(f"stockPrice: {price}, stockChange: {change}, Time: {now}")
            try:
                data = {"stockName": stock_code, "stockPrice": price,"stockChange": change}
                producer.send(topic=topicname, value=data)
                producer.flush()
            except Exception as e:
                print("could not flush", e)
            # insert_data_to_db(now, 'BRK-B', price, change)
        else:
            print("Failed to retrieve price or change.")
    else:
        print("Market has closed")
        schedule.clear()

def main(stock_code):
    print("Executing Main function at - ", datetime.now(pytz.timezone('US/Eastern')))
    while is_market_open():
        display_data(stock_code)
        time.sleep(10)
    schedule_next_market_open()


@app.route("/submit_stock_code", methods=["POST"])
def submit_stock():
    stock_code = request.json.get("stockCode")
    print("Stock code searching is: ", stock_code)
    if is_market_open():
        main(stock_code)
    else:
        # Otherwise, schedule it for the next market open
        schedule_next_market_open()
    while True:
        schedule.run_pending()
        time.sleep(1)
    # print("STOCK CODE IS ", stock_code)
    # return jsonify({"status": "success", "stockCode": stock_code})


if __name__ == "__main__":
    # If market is already open, run main immediately
    app.run(host="0.0.0.0", port=3001)
    # if is_market_open():
    #     main()
    # else:
    #     # Otherwise, schedule it for the next market open
    #     schedule_next_market_open()
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)


# CREATE TABLE stock_prices (
#     id SERIAL PRIMARY KEY,
#     timestamp TIMESTAMP NOT NULL,
#     stock_code VARCHAR(10) NOT NULL,
#     price NUMERIC(10, 2),
#     change VARCHAR(50)
# );