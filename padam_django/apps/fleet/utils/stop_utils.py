from django.utils import timezone

from ..models import BusStop
from padam_django.apps.geography.models import Place


def get_ordered_future_stops_to_place(place: Place) -> list[BusStop]:
    return (
        BusStop.objects.filter(place=place, datetime__gte=timezone.now())
        .order_by("datetime")
        .all()
    )
