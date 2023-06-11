from datetime import datetime, MINYEAR

from django.db import models
from django.db.models.query import QuerySet
from django.utils import timezone

from padam_django.apps.fleet.models.bus_stop_model import BusStop

DEFAULT_DATETIME_FOR_MISSING_STOPS = datetime(
    year=MINYEAR, month=1, day=1, tzinfo=timezone.get_current_timezone()
)


class BusShift(models.Model):
    bus = models.OneToOneField(
        "fleet.Bus", on_delete=models.CASCADE, related_name="bus"
    )
    driver = models.OneToOneField(
        "fleet.Driver", on_delete=models.CASCADE, related_name="driver"
    )
    start_datetime = models.DateTimeField(verbose_name="Shift start datetime")
    end_datetime = models.DateTimeField(verbose_name="Shift end datetime")
    total_duration = models.DurationField(verbose_name="Total shift duration")
    has_enough_stops = models.BooleanField(verbose_name="Has enough stops to be valid")

    def update_on_linked_stop_change(self):
        ordered_stops = self.get_ascending_linked_stops()
        self.update_stops_related_fields(ordered_stops)

        self.update_total_duration()

        self.save()
        return

    def update_total_duration(self) -> None:
        self.total_duration = self.end_datetime - self.start_datetime
        return

    def get_ascending_linked_stops(self) -> QuerySet[BusStop]:
        stops: QuerySet[BusStop] = self.stops.all()
        return stops.order_by("datetime")

    def update_stops_related_fields(self, ordered_stops: QuerySet[BusStop]) -> None:
        self.update_has_enough_stops(ordered_stops)
        self.update_start_datetime(ordered_stops)
        self.update_end_datetime(ordered_stops)
        return

    def update_has_enough_stops(self, stops: QuerySet[BusStop]) -> bool:
        self.has_enough_stops = len(stops) >= 2
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
