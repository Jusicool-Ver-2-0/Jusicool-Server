from django.urls import path

from market.views.list import MarketListView
from market.views.search import MarketSearchView

urlpatterns = [
    path("/list", MarketListView.as_view()),
    path("/search", MarketSearchView.as_view()),
]