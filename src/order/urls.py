from django.urls import path

from order.views.immediately import ImmediatelyBuyView, ImmediatelySellView
from order.views.month import MonthOrderView
from order.views.my import MyOrderView
from order.views.reserve import ReserveBuyView, ReserveSellView


urlpatterns = [
    # My orders
    path("/my", MyOrderView.as_view()),
    path("/month", MonthOrderView.as_view()),

    # Immediately orders
    path("/buy/<str:crypto_id>", ImmediatelyBuyView.as_view()),
    path("/sell/<str:crypto_id>", ImmediatelySellView.as_view()),

    # Reserve orders
    path("/buy/reserve/<str:crypto_id>", ReserveBuyView.as_view()),
    path("/sell/reserve/<str:crypto_id>", ReserveSellView.as_view()),
]