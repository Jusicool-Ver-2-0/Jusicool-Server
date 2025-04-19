from django.urls import path

from user.views.email import EmailRequestView, EmailValidateView
from user.views.signin import SigninView
from user.views.signup import SignupView


urlpatterns = [
    path("/signup", SignupView.as_view()),
    path("/signin", SigninView.as_view()),
    path("/email/send", EmailRequestView.as_view()),
    path("/email/verify", EmailValidateView.as_view()),
]