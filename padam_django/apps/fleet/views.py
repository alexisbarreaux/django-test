from django.http import HttpResponse
from django.utils import timezone
from django.template import loader

from .models import BusStop
from padam_django.apps.geography.models import Place


def index(request):
    return HttpResponse("Hello, world. You're at the fleet index.")


def place_stops_listing(request, place_id):
    place = Place.objects.get(pk=place_id)
    stops_at_place = (
        BusStop.objects.filter(place=place, datetime__gte=timezone.now())
        .order_by("datetime")
        .all()
    )
    template = loader.get_template("fleet/place_stops_listing.html")
    context = {"stops_at_place": stops_at_place, "place": place}
    return HttpResponse(template.render(context, request))
