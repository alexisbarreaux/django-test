from django.shortcuts import render
from django.http import HttpRequest


def bus_stop_creation(request: HttpRequest, place_id: int):
    return render(request, "fleet/bus_stop_creation.html")
