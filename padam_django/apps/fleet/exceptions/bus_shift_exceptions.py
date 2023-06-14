from padam_django.apps.fleet.models import BusShift


class BusOtherShiftsOverlapException(Exception):
    def __init__(self, shift: BusShift):
        self.shift = shift
        super().__init__(f"{shift.bus} can't be assigned to shift.")


class DriverOtherShiftsOverlapException(Exception):
    def __init__(self, shift: BusShift):
        self.shift = shift
        super().__init__(f"{shift.driver} can't be assigned to shift.")
