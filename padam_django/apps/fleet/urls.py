from django.urls import path

from . import views

app_name = "fleet"
urlpatterns = [
    path("", views.index, name="index"),
    path(
        "place/<int:place_id>/", views.place_stops_listing, name="place_stops_listing"
    ),
]
