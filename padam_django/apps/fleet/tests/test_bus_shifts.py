from datetime import datetime, timedelta

from django.test import TestCase
from django.utils import timezone

from padam_django.apps.fleet.exceptions import (
    BusOtherShiftsOverlapException,
    DriverOtherShiftsOverlapException,
    StopWouldOverlapOtherShifts,
)
from padam_django.apps.fleet.models import Bus, BusShift, BusStop, Driver
from padam_django.apps.geography.models import Place
from padam_django.apps.users.models import User


class BusShiftsHasEnoughStopsTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create()
        cls.driver_1 = Driver.objects.create(user=cls.user)

        cls.bus_1 = Bus.objects.create(licence_plate="bus_1")

        cls.shift_1 = BusShift.objects.create(bus=cls.bus_1, driver=cls.driver_1)

        cls.place_1 = Place.objects.create(name="place_1", longitude=1, latitude=1)
        super().setUpTestData()

    def test_shift_does_not_have_enough_stops_by_default(self):
        self.assertFalse(self.shift_1.has_enough_stops)

    def test_one_stop_is_not_enough_for_shift(self):
        BusStop.objects.create(
            place=self.place_1, datetime=timezone.now(), shift=self.shift_1
        )
        self.assertFalse(self.shift_1.has_enough_stops)

    def test_two_stops_is_enough_for_shift(self):
        BusStop.objects.create(
            place=self.place_1, datetime=timezone.now(), shift=self.shift_1
        )
        BusStop.objects.create(
            place=self.place_1, datetime=timezone.now(), shift=self.shift_1
        )
        self.assertTrue(self.shift_1.has_enough_stops)

    def test_deleting_stops_updates_has_enough_stops_value(self):
        BusStop.objects.create(
            place=self.place_1, datetime=timezone.now(), shift=self.shift_1
        )
        stop_2 = BusStop.objects.create(
            place=self.place_1, datetime=timezone.now(), shift=self.shift_1
        )
        self.assertTrue(self.shift_1.has_enough_stops)

        stop_2.delete()
        self.assertFalse(self.shift_1.has_enough_stops)


class BusShiftsOverlapTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_1 = User.objects.create(username="user_1")
        cls.user_2 = User.objects.create(username="user_2")

        cls.driver_1 = Driver.objects.create(user=cls.user_1)
        cls.driver_2 = Driver.objects.create(user=cls.user_2)

        cls.bus_1 = Bus.objects.create(licence_plate="bus_1")
        cls.bus_2 = Bus.objects.create(licence_plate="bus_2")

        cls.place_1 = Place.objects.create(name="place_1", longitude=1, latitude=1)

        YEAR, MONTH, DAY, HOUR = 1, 1, 1, 1

        cls.stops_overlapping_shift_1 = BusShift.objects.create(
            bus=cls.bus_1, driver=cls.driver_1
        )
        BusStop.objects.create(
            place=cls.place_1,
            datetime=datetime(
                year=YEAR, month=MONTH, day=DAY, hour=HOUR, tzinfo=timezone.utc
            ),
            shift=cls.stops_overlapping_shift_1,
        )
        BusStop.objects.create(
            place=cls.place_1,
            datetime=datetime(
                year=YEAR, month=MONTH, day=DAY, hour=HOUR + 1, tzinfo=timezone.utc
            ),
            shift=cls.stops_overlapping_shift_1,
        )

        cls.stops_overlapping_shift_2 = BusShift.objects.create(
            bus=cls.bus_2, driver=cls.driver_2
        )
        BusStop.objects.create(
            place=cls.place_1,
            datetime=datetime(
                year=YEAR, month=MONTH, day=DAY, hour=HOUR, tzinfo=timezone.utc
            ),
            shift=cls.stops_overlapping_shift_2,
        )
        BusStop.objects.create(
            place=cls.place_1,
            datetime=datetime(
                year=YEAR, month=MONTH, day=DAY, hour=HOUR + 1, tzinfo=timezone.utc
            ),
            shift=cls.stops_overlapping_shift_2,
        )

        super().setUpTestData()

    def test_switching_overlapping_shifts_to_same_bus_raises(self):
        self.stops_overlapping_shift_2.bus = self.stops_overlapping_shift_1.bus
        with self.assertRaises(BusOtherShiftsOverlapException):
            self.stops_overlapping_shift_2.save()

    def test_switching_overlapping_shifts_to_same_driver_raises(self):
        self.stops_overlapping_shift_2.driver = self.stops_overlapping_shift_1.driver
        with self.assertRaises(DriverOtherShiftsOverlapException):
            self.stops_overlapping_shift_2.save()

    def test_can_create_shift_after_other_shift_end(self):
        new_shift = BusShift.objects.create(
            bus=self.stops_overlapping_shift_1.bus,
            driver=self.stops_overlapping_shift_1.driver,
        )
        BusStop.objects.create(
            place=self.place_1,
            datetime=self.stops_overlapping_shift_1.end_datetime,
            shift=new_shift,
        )

    def test_can_create_shift_before_other_shift_start(self):
        new_shift = BusShift.objects.create(
            bus=self.stops_overlapping_shift_1.bus,
            driver=self.stops_overlapping_shift_1.driver,
        )
        BusStop.objects.create(
            place=self.place_1,
            datetime=self.stops_overlapping_shift_1.start_datetime,
            shift=new_shift,
        )

    def test_can_not_create_stop_inside_other_shift_with_same_bus(self):
        new_shift = BusShift.objects.create(
            bus=self.stops_overlapping_shift_1.bus,
            driver=self.driver_2,
        )

        with self.assertRaises(StopWouldOverlapOtherShifts):
            BusStop.objects.create(
                place=self.place_1,
                datetime=self.stops_overlapping_shift_1.end_datetime
                - timedelta(seconds=1),
                shift=new_shift,
            )

    def test_can_not_create_stop_inside_other_shift_with_same_driver(self):
        new_shift = BusShift.objects.create(
            bus=self.bus_2,
            driver=self.stops_overlapping_shift_1.driver,
        )

        with self.assertRaises(StopWouldOverlapOtherShifts):
            BusStop.objects.create(
                place=self.place_1,
                datetime=self.stops_overlapping_shift_1.end_datetime
                - timedelta(seconds=1),
                shift=new_shift,
            )

    def test_can_not_create_stop_inside_other_shift_with_same_driver_and_bus(self):
        new_shift = BusShift.objects.create(
            bus=self.stops_overlapping_shift_1.bus,
            driver=self.stops_overlapping_shift_1.driver,
        )

        with self.assertRaises(StopWouldOverlapOtherShifts):
            BusStop.objects.create(
                place=self.place_1,
                datetime=self.stops_overlapping_shift_1.end_datetime
                - timedelta(seconds=1),
                shift=new_shift,
            )

    def test_can_not_modify_stop_that_would_overlap_shift_with_same_bus(self):
        new_shift = BusShift.objects.create(
            bus=self.stops_overlapping_shift_1.bus,
            driver=self.driver_2,
        )
        new_stop = BusStop.objects.create(
            place=self.place_1,
            datetime=self.stops_overlapping_shift_1.end_datetime,
            shift=new_shift,
        )

        with self.assertRaises(StopWouldOverlapOtherShifts):
            new_stop.datetime -= timedelta(seconds=1)
            new_stop.save()

    def test_can_not_modify_stop_that_would_overlap_shift_with_same_driver(self):
        new_shift = BusShift.objects.create(
            bus=self.bus_2,
            driver=self.stops_overlapping_shift_1.driver,
        )
        new_stop = BusStop.objects.create(
            place=self.place_1,
            datetime=self.stops_overlapping_shift_1.end_datetime,
            shift=new_shift,
        )

        with self.assertRaises(StopWouldOverlapOtherShifts):
            new_stop.datetime -= timedelta(seconds=1)
            new_stop.save()

    def test_can_not_modify_stop_that_would_overlap_shift_with_same_driver_and_bus(
        self,
    ):
        new_shift = BusShift.objects.create(
            bus=self.stops_overlapping_shift_1.bus,
            driver=self.stops_overlapping_shift_1.driver,
        )
        new_stop = BusStop.objects.create(
            place=self.place_1,
            datetime=self.stops_overlapping_shift_1.end_datetime,
            shift=new_shift,
        )

        with self.assertRaises(StopWouldOverlapOtherShifts):
            new_stop.datetime -= timedelta(seconds=1)
            new_stop.save()
