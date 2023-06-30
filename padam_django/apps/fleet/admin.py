from django.contrib import admin

from . import models


@admin.register(models.Bus)
class BusAdmin(admin.ModelAdmin):
    pass


class BusStopsInline(admin.TabularInline):
    model = models.BusStop
    ordering = ("datetime",)


@admin.register(models.BusShift)
class BusShiftAdmin(admin.ModelAdmin):
    def has_enough_stops(self, instance: models.BusShift) -> bool:
        """
        Wrapper to keep has_enough_stops as property in the Model but have a nice
        display in admin
        """
        return instance.has_enough_stops

    has_enough_stops.boolean = True

    readonly_fields = (
        "total_duration",
        "start_datetime",
        "end_datetime",
        "has_enough_stops",
    )
    fieldsets = [
        (
            "Main",
            {
                "fields": [
                    "bus",
                    "driver",
                    "start_datetime",
                    "end_datetime",
                    "total_duration",
                ]
            },
        ),
        ("Flags", {"fields": ["has_enough_stops"]}),
    ]
    inlines = [BusStopsInline]


@admin.register(models.Driver)
class DriverAdmin(admin.ModelAdmin):
    pass


@admin.register(models.BusStop)
class BusStopAdmin(admin.ModelAdmin):
    pass
