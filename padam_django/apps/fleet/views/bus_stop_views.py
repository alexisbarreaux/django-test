from django.http import HttpRequest
from django.shortcuts import get_object_or_404, render

from padam_django.apps.geography.models import Place

from ..exceptions import BusStopAlreadyExistsError
from ..forms import BusStopCreationForm
from ..models import BusStop
from ..utils import bus_stop_already_exists, get_shift_for_new_stop


def bus_stop_creation(request: HttpRequest, place_id: int):
    place = get_object_or_404(Place, pk=place_id)

    if request.method == "POST":
        form = BusStopCreationForm(request.POST)
        if form.is_valid():
            datetime = form.cleaned_data["datetime"]
            new_bus_stop = BusStop(datetime=datetime, place=place)

            if bus_stop_already_exists(datetime=datetime, place=place):
                form.add_error("datetime", BusStopAlreadyExistsError(stop=new_bus_stop))
            else:
                new_bus_stop.shift = get_shift_for_new_stop(new_bus_stop)
                new_bus_stop.save()
                return render(
                    request,
                    "fleet/bus_stop_creation_success.html",
                    {"place": place, "datetime": datetime},
                )
    else:
        form = BusStopCreationForm(initial={"place": str(place)})

    return render(
        request, "fleet/bus_stop_creation.html", {"form": form, "place": place}
    )
