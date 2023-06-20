from django.shortcuts import render


def bus_stop_creation(request):
    return render(request, "fleet/bus_stop_creation.html")
