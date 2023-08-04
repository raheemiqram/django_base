from django.urls import path
from .views import TradeView

urlpatterns = [
    path('binance-spot/', TradeView.as_view(), name='trading-list'),
]
