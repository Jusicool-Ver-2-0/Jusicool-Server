from django.urls import path

from market.views.market import MarketView

urlpatterns = [
    path("", MarketView().as_view()),
]