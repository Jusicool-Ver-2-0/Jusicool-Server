from django.urls import path

from crypto.views.crypto import CryptoView

urlpatterns = [
    path("", CryptoView().as_view()),
]