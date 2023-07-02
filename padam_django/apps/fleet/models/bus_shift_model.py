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
    start_datetime = models.DateTimeField(
        verbose_name="Shift start datetime", default=DEFAULT_DATETIME_FOR_MISSING_STOPS
    )
    end_datetime = models.DateTimeField(
        verbose_name="Shift end datetime", default=DEFAULT_DATETIME_FOR_MISSING_STOPS
    )

    @property
    def has_enough_stops(self) -> bool:
        return self.stops.count() >= 2

    @property
    def total_duration(self) -> timedelta:
        return self.end_datetime - self.start_datetime

    def save(self, *args, **kwargs):
        ordered_stops = self.get_ascending_linked_stops()
        self.update_stops_related_fields(ordered_stops)
        return super().save(*args, **kwargs)

    def get_ascending_linked_stops(self) -> QuerySet[BusStop]:
        stops: QuerySet[BusStop] = self.stops.all()
        return stops.order_by("datetime")

    def update_stops_related_fields(self, ordered_stops: QuerySet[BusStop]) -> None:
        self.update_start_datetime(ordered_stops)
        self.update_end_datetime(ordered_stops)
        return

    def update_start_datetime(self, ordered_stops: QuerySet[BusStop]) -> None:
        first_stop: BusStop = ordered_stops.first()
        if first_stop is not None:
            self.start_datetime = first_stop.datetime
        else:
            self.start_datetime = DEFAULT_DATETIME_FOR_MISSING_STOPS
        return

    def update_end_datetime(self, ordered_stops: QuerySet[BusStop]) -> None:
        last_stop: BusStop = ordered_stops.last()
        if last_stop is not None:
            self.end_datetime = last_stop.datetime
        else:
            self.end_datetime = DEFAULT_DATETIME_FOR_MISSING_STOPS
        return

    def __str__(self):
        return f"BusShift: {self.bus} by {self.driver} from {self.start_datetime} to {self.end_datetime} (id: {self.pk})"
