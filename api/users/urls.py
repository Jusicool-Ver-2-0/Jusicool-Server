from django.urls import path

from api.users.views import EmailVerificationAPIView

urlpatterns = [
    path(
        "email-verification",
        EmailVerificationAPIView.as_view(),
        name="email-verification",
    ),
]
