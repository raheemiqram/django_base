import time
from datetime import datetime

from binance.client import Client
import numpy as np
from sklearn.linear_model import LinearRegression

api_key = 'qzDUhfOy3EDZaTwlgcA6fS36sMhZvOAEOEYQ6ccu8iOTZCrrXZOZHpe220DoogD8'
api_secret = 'S7LMYlcvlnkV7uuL012Tcu7KYf4cRTz8xq5bfdkOXmkYB4do4lWB0iC9IlOCamO3'

client = Client(api_key, api_secret)


def get_future_current_market_price(symbol):
    ticker = client.futures_ticker(symbol=symbol)
    return float(ticker['lastPrice'])


def get_spot_current_market_price(symbol):
    ticker = client.get_symbol_ticker(symbol=symbol)
    return float(ticker['price'])


def place_order(symbol, side, quantity, price, order_type=Client.ORDER_TYPE_MARKET):
    order = client.futures_create_order(
        symbol=symbol,
        side=side,
        type=order_type,
        quantity=quantity,
        price=price,
        timeInForce=Client.TIME_IN_FORCE_GTC
    )
    return order


def predict_future_price(symbol, window_size=10):
    klines = client.futures_klines(symbol=symbol, interval=Client.KLINE_INTERVAL_1MINUTE)
    closes = np.array([float(kline[4]) for kline in klines])

    # Create input data for the linear regression model
    X = np.arange(len(closes)).reshape(-1, 1)
    y = closes

    # Train the linear regression model
    model = LinearRegression()
    model.fit(X, y)

    # Predict the future price using the linear regression model
    future_price = model.predict(np.array(len(closes)).reshape(-1, 1))[0]

    return future_price


def spot_predict_future_price(symbol):
    # Get the last kline for the specified trading pair
    klines = client.get_historical_klines(symbol, Client.KLINE_INTERVAL_1MINUTE, '1 minute ago')
    last_kline = klines[-2]

    # Get the closing price of the last kline
    last_close = float(last_kline[4])

    # Get the timestamp of the last kline and add one minute
    last_timestamp = int(last_kline[0])
    next_timestamp = last_timestamp + 60000

    # Get the kline for the next minute
    next_klines = client.get_historical_klines(symbol, Client.KLINE_INTERVAL_1MINUTE,
                                               datetime.fromtimestamp(next_timestamp / 1000).strftime(
                                                   '%Y-%m-%d %H:%M:%S'))
    next_close = float(next_klines[0][4])

    # Train the linear regression model using the historical data
    X = np.array([0, 1]).reshape(-1, 1)
    y = np.array([last_close, next_close])
    model = LinearRegression()
    model.fit(X, y)

    # Predict the price after one minute
    future_price = model.predict([[2]])[0]

    return future_price


def predict_and_trade(symbol, window_size=10, threshold=0.01):
    # Predict future price using linear regression model
    future_price = predict_future_price(symbol, window_size)
    entry_price = float(client.futures_symbol_ticker(symbol=symbol)['price'])

    if future_price / entry_price > 1 + threshold:
        # Buy if predicted price is higher than current price by threshold amount
        # order = client.futures_create_order(symbol=symbol, side=Client.SIDE_BUY, type=Client.ORDER_TYPE_MARKET,
        #                                     quantity=10)
        order = {'price': entry_price}
        trade_type = 'buy'
    elif future_price / entry_price < 1 - threshold:
        # Sell if predicted price is lower than current price by threshold amount
        # order = client.futures_create_order(symbol=symbol, side=Client.SIDE_SELL, type=Client.ORDER_TYPE_MARKET,
        #                                     quantity=10)
        trade_type = 'sell'
        order = {'price': entry_price}
    else:
        # Hold if predicted price is within threshold of current price
        trade_type = 'hold'
        order = {'price': entry_price}

    time.sleep(60)

    # Check actual price change and determine win or loss
    current_price = float(client.futures_symbol_ticker(symbol=symbol)['price'])
    if trade_type == 'buy':
        if current_price > order['price']:
            result = 'win'
        else:
            result = 'loss'
    elif trade_type == 'sell':
        if current_price < order['price']:
            result = 'win'
        else:
            result = 'loss'
    else:
        result = 'hold'

    results = {"result": result, "entry_price": entry_price, "predict_price": future_price,
               "current_price": current_price}

    return results


def predict_future_price_test(symbol, window_size=10):
    klines = client.futures_klines(symbol=symbol, interval=Client.KLINE_INTERVAL_1MINUTE)
    closes = np.array([float(kline[4]) for kline in klines])

    # Create input data for the linear regression model
    X = np.arange(len(closes)).reshape(-1, 1)
    y = closes

    # Train the linear regression model
    model = LinearRegression()
    model.fit(X, y)

    while True:
        # Get the current price
        ticker = client.futures_symbol_ticker(symbol=symbol)
        current_price = float(ticker['price'])

        # Predict the future price using the linear regression model
        future_price = model.predict(np.array(len(closes)).reshape(-1, 1))[0]

        # Determine if the predicted price is higher or lower than the current price
        if future_price > current_price:
            result = 'win'
        else:
            result = 'loose'

        print(f'Predicted price: {future_price:.2f}, Current price: {current_price:.2f}, Result: {result}')

        # Wait for 60 seconds before making the next prediction
        time.sleep(60)
