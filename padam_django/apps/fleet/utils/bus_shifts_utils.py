from datetime import datetime

from django.db.models.query import QuerySet

from ..exceptions import NoShiftsAvailable
from ..models import BusShift, BusStop


def get_shift_for_new_stop(stop: BusStop) -> BusShift:
    if no_shift_is_available():
        raise NoShiftsAvailable
    elif (
        active_shift_for_stop := get_shift_active_at_datetime(stop.datetime)
    ) is not None:
        return active_shift_for_stop
    else:
        return get_shift_closest_to_datetime(stop.datetime)


def no_shift_is_available() -> bool:
    return not BusShift.objects.exists()


def get_shift_active_at_datetime(datetime: datetime) -> BusShift:
    active_shifts_for_stop = get_shifts_active_at_datetime(datetime)
    if active_shifts_for_stop.exists():
        return active_shifts_for_stop.first()
    else:
        return None


def get_shifts_active_at_datetime(datetime: datetime) -> QuerySet[BusShift]:
    return BusShift.objects.filter(
        start_datetime__lt=datetime, end_datetime__gt=datetime
    )


def get_shift_closest_to_datetime(datetime: datetime) -> BusShift:
    start_closest_shift = get_shift_with_closest_start_after_datetime(datetime)
    end_closest_shift = get_shift_with_closest_end_before_datetime(datetime)

    if end_closest_shift is None:
        return start_closest_shift
    elif start_closest_shift is None:
        return end_closest_shift
    else:
        end_delta = datetime - end_closest_shift.end_datetime
        start_delta = start_closest_shift.start_datetime - datetime
        if end_delta < start_delta:
            return end_closest_shift
        else:
            return start_closest_shift


def get_shift_with_closest_start_after_datetime(datetime: datetime) -> BusShift:
    return (
        BusShift.objects.filter(start_datetime__gt=datetime)
        .order_by("start_datetime")
        .first()
    )


def get_shift_with_closest_end_before_datetime(datetime: datetime) -> BusShift:
    return (
        BusShift.objects.filter(end_datetime__lt=datetime)
        .order_by("-end_datetime")
        .first()
    )
