from padam_django.apps.fleet.models import BusShift


class ShiftsOverlapException(Exception):
    shift: BusShift

    def __init__(self, shift: BusShift):
        self.shift = shift
        super().__init__(
            f"Changes to shift with id {shift.pk} would overlap other shifts. "
            + self.overlap_reason()
        )

    def overlap_reason(self) -> str:
        raise NotImplementedError


class BusOtherShiftsOverlapException(ShiftsOverlapException):
    def overlap_reason(self) -> str:
        return f"{self.shift.bus} would be conflicted."


class DriverOtherShiftsOverlapException(ShiftsOverlapException):
    def overlap_reason(self) -> str:
        return f"{self.shift.driver} would be conflicted."
