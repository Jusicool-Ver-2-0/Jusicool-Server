from django.urls import path

from crypto.views.list import CryptoListView


urlpatterns = [
    path("/list", CryptoListView.as_view()),
]