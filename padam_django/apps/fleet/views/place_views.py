from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from ..utils import get_ordered_future_stops_to_place
from padam_django.apps.geography.models import Place


def place_choosing(request) -> HttpResponse:
    places = Place.objects.all()
    print(places)
    return render(request, "fleet/place_choosing.html", {"places": places})


def place_stops_listing(request, place_id) -> HttpResponse:
    place: Place = get_object_or_404(Place, pk=place_id)

    stops_at_place = get_ordered_future_stops_to_place(place=place)

    context = {"stops_at_place": stops_at_place, "place": place}

    return render(request, "fleet/place_stops_listing.html", context)
