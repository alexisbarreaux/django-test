from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path(
        "place/<int:place_id>/", views.place_stops_listing, name="place_stops_listing"
    ),
]
