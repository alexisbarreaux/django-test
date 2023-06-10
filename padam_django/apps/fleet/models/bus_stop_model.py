from django.db import models


class BusStop(models.Model):
    place = models.OneToOneField(
        "geography.Place", on_delete=models.CASCADE, related_name="place"
    )
    datetime = models.DateTimeField(verbose_name="Bus stop datetime", auto_now_add=True)
    shift = models.OneToOneField(
        "fleet.BusShift", on_delete=models.CASCADE, related_name="bus_shift"
    )

    def __str__(self):
        return f"BusStop: {self.place} the {self.datetime.date()} at {self.datetime.time()} (id: {self.pk})"
