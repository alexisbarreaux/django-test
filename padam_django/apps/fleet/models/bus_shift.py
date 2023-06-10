from django.db import models


class BusShift(models.Model):
    bus = models.OneToOneField(
        "fleet.Bus", on_delete=models.CASCADE, related_name="bus"
    )
    driver = models.OneToOneField(
        "fleet.Driver", on_delete=models.CASCADE, related_name="driver"
    )
    start_datetime = models.DateTimeField(verbose_name="Shift start datetime")
    end_datetime = models.DateTimeField(verbose_name="Shift end datetime")

    def __str__(self):
        return f"BusShift: {self.bus} by {self.driver} from {self.start_datetime} to {self.end_datetime} (id: {self.pk})"
