from django.db.models.signals import post_save
from django.dispatch import receiver

from padam_django.apps.fleet.exceptions import (
    BusOtherShiftsOverlapException,
    DriverOtherShiftsOverlapException,
)
from padam_django.apps.fleet.models import BusShift
from padam_django.apps.fleet.utils import is_shift_set_overlapping_other_shift


@receiver(post_save, sender=BusShift)
def ensure_overlapping_is_fine(
    sender, instance: BusShift, using, update_fields, **kwargs
):
    instance_bus_other_shifts = instance.bus.shifts.exclude(pk=instance.pk)
    instance_driver_other_shifts = instance.driver.shifts.exclude(pk=instance.pk)
    if is_shift_set_overlapping_other_shift(
        shifts_set=instance_bus_other_shifts, other_shift=instance
    ):
        raise BusOtherShiftsOverlapException(instance)
    elif is_shift_set_overlapping_other_shift(
        shifts_set=instance_driver_other_shifts, other_shift=instance
    ):
        raise DriverOtherShiftsOverlapException(instance)
    else:
        return
