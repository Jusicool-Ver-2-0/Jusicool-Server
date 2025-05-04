from django.urls import path

from holding.views.my import MyHoldingView


urlpatterns = [
    path("/my", MyHoldingView.as_view()),
]