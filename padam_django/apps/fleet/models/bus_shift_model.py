from datetime import MINYEAR, datetime, timedelta

from django.db import models
from django.db.models.query import QuerySet
from django.utils import timezone

from padam_django.apps.fleet.models.bus_stop_model import BusStop

DEFAULT_DATETIME_FOR_MISSING_STOPS = datetime(
    year=MINYEAR, month=1, day=1, tzinfo=timezone.get_current_timezone()
)


class BusShift(models.Model):
    bus = models.ForeignKey(
        "fleet.Bus", on_delete=models.CASCADE, related_name="shifts"
    )
    driver = models.ForeignKey(
        "fleet.Driver", on_delete=models.CASCADE, related_name="shifts"
    )

    @property
    def has_enough_stops(self) -> bool:
        return self.stops.count() >= 2

    @property
    def start_datetime(self) -> datetime:
        try:
            return self.get_ascending_linked_stops().first().datetime
        except AttributeError:
            return DEFAULT_DATETIME_FOR_MISSING_STOPS

    @property
    def end_datetime(self) -> datetime:
        try:
            return self.get_ascending_linked_stops().last().datetime
        except AttributeError:
            return DEFAULT_DATETIME_FOR_MISSING_STOPS

    @property
    def total_duration(self) -> timedelta:
        return self.end_datetime - self.start_datetime

    def get_ascending_linked_stops(self) -> QuerySet[BusStop]:
        stops: QuerySet[BusStop] = self.stops.all()
        return stops.order_by("datetime")

    def __str__(self):
        return f"BusShift: {self.bus} by {self.driver} from {self.start_datetime} to {self.end_datetime} (id: {self.pk})"
