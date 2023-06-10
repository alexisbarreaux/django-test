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
    fieldsets = [
        ("Main", {"fields": ["bus", "driver", "start_datetime", "end_datetime"]}),
    ]
    inlines = [BusStopsInline]


@admin.register(models.Driver)
class DriverAdmin(admin.ModelAdmin):
    pass


@admin.register(models.BusStop)
class BusStopAdmin(admin.ModelAdmin):
    pass
