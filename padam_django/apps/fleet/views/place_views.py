from typing import Any
from django.http import HttpResponseRedirect, HttpRequest
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views import generic

from ..utils import get_ordered_future_stops_to_place
from padam_django.apps.geography.models import Place


class PlaceChoosingView(generic.ListView):
    template_name = "fleet/place_choosing.html"
    context_object_name = "places"
    place: Place

    def get_queryset(self):
        return Place.objects.all()


class PlaceStopsListingView(generic.ListView):
    template_name = "fleet/place_stops_listing.html"
    context_object_name = "stops_at_place"
    place: Place

    def setup(self, request: HttpRequest, *args: Any, **kwargs: Any) -> None:
        super().setup(request, *args, **kwargs)
        self.place = get_object_or_404(Place, pk=self.kwargs["place_id"])
        return

    def get_queryset(self):
        return get_ordered_future_stops_to_place(place=self.place)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["place"] = self.place
        return context


def place_choice_handling(request: HttpRequest) -> HttpResponseRedirect:
    return HttpResponseRedirect(
        reverse("fleet:place_stops_listing", args=(request.POST["place_id"],))
    )
