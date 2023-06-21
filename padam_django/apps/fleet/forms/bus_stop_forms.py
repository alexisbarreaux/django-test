from django.forms import DateTimeField, DateTimeInput, Form
from django.utils import timezone

from ..exceptions import BusStopPastDatetimeError


class BusStopCreationForm(Form):
    datetime = DateTimeField(
        widget=DateTimeInput(attrs={"type": "datetime-local"}),
        label="Choose desired date and time for the stop.",
    )

    def clean_datetime(self):
        datetime = self.cleaned_data["datetime"]
        if datetime < timezone.now():
            raise BusStopPastDatetimeError

        return datetime
