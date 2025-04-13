from django.urls import path

from accounts.views.signup import SignupView

urlpatterns = [
    path("/signup", SignupView.as_view()),
]