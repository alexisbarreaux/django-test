from django.http import HttpRequest
from django.shortcuts import get_object_or_404, render

from padam_django.apps.fleet.forms import BusStopCreationForm
from padam_django.apps.geography.models import Place


def bus_stop_creation(request: HttpRequest, place_id: int):
    place = get_object_or_404(Place, pk=place_id)

    if request.method == "POST":
        print(request.POST)
        form = BusStopCreationForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
    else:
        form = BusStopCreationForm(initial={"place": str(place)})
    return render(
        request, "fleet/bus_stop_creation.html", {"form": form, "place": place}
    )
