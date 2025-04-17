from django.urls import path

from crypto.views.candle import CryptoCandleView
from crypto.views.crypto import CryptoView
from crypto.views.tick import CryptoTickView

urlpatterns = [
    path("", CryptoView.as_view()),
    path("/candle/<str:time>", CryptoCandleView.as_view()),
    path("/tick/<str:crypto_code>", CryptoTickView.as_view()),
]