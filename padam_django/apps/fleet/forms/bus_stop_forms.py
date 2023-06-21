from django.forms import ModelForm, Select, TextInput, ValidationError
from django.utils import timezone

from padam_django.apps.fleet.models import BusStop


class BusStopCreationForm(ModelForm):
    class Meta:
        model = BusStop
        fields = ["datetime"]
        widgets = {
            "datetime": TextInput(attrs={"type": "datetime-local"}),
        }

    def clean_datetime(self):
        datetime = self.cleaned_data["datetime"]
        if datetime < timezone.now():
            raise ValidationError(
                "Our drivers are the best, but they won't be able to come get you in the past."
            )
        return datetime
