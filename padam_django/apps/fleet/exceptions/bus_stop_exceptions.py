from django.forms import ValidationError

from ..models import BusStop


class StopWouldOverlapOtherShifts(Exception):
    def __init__(self, stop: BusStop):
        self.stop = stop
        super().__init__(
            f"Can't set stop {stop.pk} to {stop.datetime}. Would overlap other shifts."
        )


class BusStopPastDatetimeError(ValidationError):
    def __init__(self) -> None:
        super().__init__(
            message=(
                "Our drivers are the best, but they won't be able to come get you in the past."
            )
        )


class BusStopAlreadyExistsError(ValidationError):
    def __init__(self, stop: BusStop) -> None:
        super().__init__(
            message=(f"A stop at {stop.place} on {stop.datetime} already exists.")
        )
