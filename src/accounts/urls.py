from django.urls import path

from accounts.views.email import EmailView
from accounts.views.signup import SignupView

urlpatterns = [
    path("/signup", SignupView.as_view()),
    path("/email", EmailView.as_view()),
]