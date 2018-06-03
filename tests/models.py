from django.db import models


class Location(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
