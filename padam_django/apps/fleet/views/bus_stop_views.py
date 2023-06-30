from django.forms import ValidationError
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from padam_django.apps.geography.models import Place

from ..exceptions import (
    BusStopAlreadyExistsError,
    NoShiftsAvailable,
    NoShiftsAvailableError,
)
from ..forms import BusStopCreationForm
from ..models import BusStop
from ..utils import bus_stop_already_exists, get_shift_for_given_datetime


def bus_stop_creation(request: HttpRequest, place_id: int) -> HttpResponse:
    place = get_object_or_404(Place, pk=place_id)

    if request.method == "POST":
        form = BusStopCreationForm(request.POST)
        if form.is_valid():
            try:
                new_bus_stop = BusStop(
                    datetime=form.cleaned_data["datetime"], place=place
                )
                add_shift_to_stop(stop=new_bus_stop)
                check_stop_validity(stop=new_bus_stop)
                new_bus_stop.save()
            except ValidationError as e:
                form.add_error("datetime", e)
            else:
                return redirect(
                    "fleet:bus_stop_creation_success",
                    args=(new_bus_stop.place.pk,),
                )
    else:
        form = BusStopCreationForm(initial={"place": str(place)})

    return render(
        request, "fleet/bus_stop_creation.html", {"form": form, "place": place}
    )


def add_shift_to_stop(stop: BusStop) -> None:
    try:
        shift = get_shift_for_given_datetime(stop.datetime)
        stop.shift = shift
        return
    except NoShiftsAvailable:
        raise NoShiftsAvailableError


def check_stop_validity(stop: BusStop) -> None:
    if bus_stop_already_exists(stop=stop):
        raise BusStopAlreadyExistsError(stop=stop)
    else:
        return


def bus_stop_creation_success(request: HttpRequest, place_id: int) -> HttpResponse:
    place = get_object_or_404(Place, pk=place_id)
    return render(
        request,
        "fleet/bus_stop_creation_success.html",
        {"place": place},
    )
