import json
import os
import folium
from folium.plugins import FastMarkerCluster, MarkerCluster
from django.db import connection
from django.test import TestCase
from georangefilter import filter_in_range
from tests.models import Location

REAL_DIR = os.path.dirname(os.path.realpath(__file__))


class GeoRangeFilterTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        """
        Create extensions.
        """
        super().setUpClass()
        cursor = connection.cursor()
        cursor.execute("CREATE EXTENSION IF NOT EXISTS cube;")
        cursor.execute("CREATE EXTENSION IF NOT EXISTS earthdistance;")

    @classmethod
    def setUpTestData(cls):
        """
        Load locations from a real map.
        """
        cls.locations = json.load(open(os.path.join(REAL_DIR, "data/pllocations.json")))
        # create test models
        for x in cls.locations:
            Location(latitude=x[0], longitude=x[1]).save()
        # center of our map, from which we draw a circle
        cls.location = [52.91228, 19.12048]

    def _test_in_range(self, in_range, add_circle=0, save_map=False):
        city = self.location.copy()  # place in the middle of Poland
        # filter in range
        locations_in_range = filter_in_range(
            queryset=Location.objects.all(),
            latitude=city[0],
            longitude=city[1],
            range_in_meters=in_range,
            field_name="geobox",
        )
        if save_map:
            # create map
            mapit = folium.Map(location=[city[0], city[1]], zoom_start=7.5, control_scale=True)
            # create circles
            folium.features.Circle(
                radius=in_range, location=city, color="crimson", fill=False
            ).add_to(mapit)
            # create second cirlce
            folium.features.Circle(
                radius=in_range + add_circle,
                location=city,
                color="#3186cc",
                fill=True,
                fill_color="#3186cc",
            ).add_to(mapit)
            # fast marker for a lot of points
            # FastMarkerCluster(
            #     [[x.latitude, x.longitude] for x in locations_in_range]
            # ).add_to(mapit)
            # add locations to map
            for x in locations_in_range:
                folium.Marker((x.latitude, x.longitude)).add_to(mapit)
            # open file for write
            f = open(
                os.path.join(
                    REAL_DIR, "maps/locations_{0}_range.html".format(in_range)
                ),
                "wb",
            )
            # save map to file
            mapit.save(f)

        return locations_in_range

    def test_models_are_created(self):
        self.assertEqual(len(Location.objects.all()), len(self.locations))

    def test_filter_in_range_save_map(self):
        in_range = 15000
        self._test_in_range(in_range, in_range, save_map=True)
