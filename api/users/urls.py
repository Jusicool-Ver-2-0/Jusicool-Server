from django.urls import path

from api.users.views import EmailRequestView

urlpatterns = [
    path(
        "/email/send",
        EmailRequestView.as_view(),
        name="email-send",
    ),
]
