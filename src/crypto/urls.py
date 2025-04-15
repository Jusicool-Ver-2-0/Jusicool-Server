from django.urls import path

from crypto.views.candle import CryptoCandleView
from crypto.views.crypto import CryptoView

urlpatterns = [
    path("", CryptoView.as_view()),
    path("/candle/<str:time>", CryptoCandleView.as_view()),
]