from django.urls import path

from .views import ContactView, DatenschutzView, ImpressumView, IndexView, NeupatientenView

app_name = "base"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("neupatienten/", NeupatientenView.as_view(), name="neupatienten"),
    path("impressum/", ImpressumView.as_view(), name="impressum"),
    path("datenschutz/", DatenschutzView.as_view(), name="datenschutz"),
    path("contact/", ContactView.as_view(), name="contact"),
]
