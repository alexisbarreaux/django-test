from padam_django.apps.fleet.models import BusStop


class StopWouldOverlapOtherShifts(Exception):
    def __init__(self, stop: BusStop):
        self.stop = stop
        super().__init__(
            f"Can't set stop {stop.pk} to {stop.datetime}. Would overlap other shifts."
        )
