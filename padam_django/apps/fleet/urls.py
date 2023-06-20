from django.urls import path

from . import views

app_name = "fleet"
urlpatterns = [
    path("", views.index, name="index"),
    path("place/", views.PlaceChoosingView.as_view(), name="place_choosing"),
    path("chose_place/", views.place_choice_handling, name="chose_place"),
    path(
        "place/<int:place_id>/",
        views.PlaceStopsListingView.as_view(),
        name="place_stops_listing",
    ),
    path(
        "bus_stop/add/place=<int:place_id>/",
        views.bus_stop_creation,
        name="bus_stop_creation",
    ),
]
