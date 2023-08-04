from binance import Client
from django.views.generic import TemplateView

from apps.trading_bot.utils import *


class TradeView(TemplateView):
    template_name = 'dashboard/trading_bot/trade.html'

    def get_context_data(self, **kwargs):
        # Get the current price of the futures contract
        context = super().get_context_data(**kwargs)

        symbol = 'BTCUSDT'
        # current_price = get_future_current_market_price(symbol)
        # future_price = predict_future_price(symbol=symbol)
        results = predict_and_trade(symbol=symbol)
        # Determine whether to buy or sell based on the price trend
        # predicted_price = predict_future_price(symbol, 1)
        # if predicted_price > current_price:
        #     place_order(symbol, Client.SIDE_BUY, quantity, current_price)
        # elif predicted_price < current_price:
        #     place_order(symbol, Client.SIDE_SELL, quantity, current_price)
        #
        # # Add the price and trading action to the context
        # context = super().get_context_data(**kwargs)
        # context['price'] = price
        # context['action'] = 'Buy' if price > prev_price else 'Sell'
        context['current_price'] = "current_price"
        context['future_price'] = "future_price"
        context['results'] = results
        return context
