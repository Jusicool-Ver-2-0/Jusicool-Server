from django.urls import path

from accounts.views.email import EmailView
from accounts.views.signin import SigninView
from accounts.views.signup import SignupView

urlpatterns = [
    path("/signup", SignupView.as_view()),
    path("/signin", SigninView.as_view()),
    path("/email", EmailView.as_view())
]