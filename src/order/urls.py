from django.urls import path

from order.views.immediately import ImmediatelyBuyView, ImmediatelySellView
from order.views.month import MonthOrderView, MonthRateView
from order.views.my import MyOrderView
from order.views.reserve import ReserveBuyView, ReserveSellView


urlpatterns = [
    # My orders
    path("/my", MyOrderView.as_view()),
    path("/month", MonthOrderView.as_view()),
    path("/month/rate", MonthRateView.as_view()),
    # Immediately orders
    path("/buy/<str:market>", ImmediatelyBuyView.as_view()),
    path("/sell/<str:market>", ImmediatelySellView.as_view()),
    # Reserve orders
    path("/buy/reserve/<str:market>", ReserveBuyView.as_view()),
    path("/sell/reserve/<str:market>", ReserveSellView.as_view()),
]
