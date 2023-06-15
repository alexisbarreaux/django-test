from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from padam_django.apps.fleet.models import BusStop
from padam_django.apps.fleet.exceptions import (
    ShiftsOverlapException,
    StopWouldOverlapOtherShifts,
)


@receiver(post_delete, sender=BusStop)
@receiver(post_save, sender=BusStop)
def update_linked_shift(sender, instance: BusStop, using, **kwargs):
    try:
        instance.shift.save()
    except ShiftsOverlapException as e:
        raise StopWouldOverlapOtherShifts(instance) from e
    return
