from django.urls import path

from account.views.my import MyAccountView


urlpatterns = [
    path("/my", MyAccountView.as_view()),
]
