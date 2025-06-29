from django.urls import path

from .views import ContactView, IndexView

app_name = "base"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("contact/", ContactView.as_view(), name="contact"),
]
