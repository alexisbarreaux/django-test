from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from padam_django.apps.fleet.models import BusStop
from padam_django.apps.fleet.exceptions import (
    DriverOtherShiftsOverlapException,
    BusOtherShiftsOverlapException,
    StopWouldOverlapOtherShifts,
)


@receiver(post_delete, sender=BusStop)
@receiver(post_save, sender=BusStop)
def update_linked_shift(sender, instance: BusStop, using, **kwargs):
    try:
        instance.shift.save()
    except (DriverOtherShiftsOverlapException, BusOtherShiftsOverlapException) as e:
        raise StopWouldOverlapOtherShifts(
            f"Can't set stop {instance.pk} to {instance.datetime}. Would overlap other shifts."
        ) from e
    return
