from django.urls import path

from exchange.views.exchange import ExchangeView


urlpatterns = [
    path("/<str:exchange_type>", ExchangeView.as_view()),

]