from django.urls import path

from accounts.views.email import EmailRequestView, EmailValidateView
from accounts.views.signin import SigninView
from accounts.views.signup import SignupView

urlpatterns = [
    path("/signup", SignupView.as_view()),
    path("/signin", SigninView.as_view()),
    path("/email/send", EmailRequestView.as_view()),
    path("/email/verify", EmailValidateView.as_view()),
]