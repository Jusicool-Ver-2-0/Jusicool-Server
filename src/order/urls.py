from django.urls import path

from order.views.crypto import CryptoBuyView, CryptoSellView
from order.views.crypto_my import CryptoMyOrderView
from order.views.crypto_reserve import CryptoReserveBuyView, CryptoReserveSellView

urlpatterns = [
    path("/crypto/my", CryptoMyOrderView.as_view()),
    path("/crypto/buy/<str:crypto_id>", CryptoBuyView.as_view()),
    path("/crypto/sell/<str:crypto_id>", CryptoSellView.as_view()),
    path("/crypto/reserve/buy/<str:crypto_id>", CryptoReserveBuyView.as_view()),
    path("/crypto/reserve/sell/<str:crypto_id>", CryptoReserveSellView.as_view()),
]