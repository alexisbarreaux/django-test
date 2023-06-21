from datetime import datetime

from django.utils import timezone

from padam_django.apps.geography.models import Place

from ..models import BusStop


def get_ordered_future_stops_to_place(place: Place) -> list[BusStop]:
    return (
        BusStop.objects.filter(place=place, datetime__gte=timezone.now())
        .order_by("datetime")
        .all()
    )


def bus_stop_already_exists(datetime: datetime, place: Place) -> bool:
    return BusStop.objects.filter(datetime=datetime, place=place).exists()
