from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path(
        "jadmin/",
        admin.site.urls,
    ),
    path(
        "api/",
        include("api.urls"),
        name="api",
    ),
    path(
        "_api/",
        include("internal_api.urls"),
        name="internal_api",
    ),
]
