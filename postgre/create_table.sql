create table stock_opens(
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(255) NOT NULL,
    average_open_per_10_day DOUBLE PRECISION,
    dates DATETIME NOT NULL
)