from django.urls import path

from market.views.list import MarketListView


urlpatterns = [
    path("/list", MarketListView.as_view()),
]