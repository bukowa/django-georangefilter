# django-georangefilter
Python function that will annonate your queryset using Postgres **earth_box** and **ll_to_earth** functions that allow filtering in range N kilometers from given latitude/longitude point.<br>
**IMPORTANT:**<br>https://www.postgresql.org/docs/devel/static/earthdistance.html<br>
```
In this module, the Earth is assumed to be perfectly spherical. (If that's too inaccurate for you, you might want to look at the PostGIS project).
```
[Tests results are here](tests/maps): increasing the range of the filter by 10km each time, first circle is the **range** and the second cirle is **range x 2**(so for 10km radius, second circle is 20km radius)<br>
````
If you want to test in your custom radius, take a look at tests.py file.
````
<br>For example, given model:
```python
class City(models.Model):
    longitude = models.FloatField(db_index=True)
    latitude = models.FloatField(db_index=True)
    
    def in_range(self, range_in_meters, **kwargs):
        return filter_in_range(
            queryset=self.__class__.objects,
            latitude=self.latitude,
            longitude=self.longitude,
            range_in_meters=range_in_meters,
            latitude_column_name="latitude",
            longitude_column_name="longitude",
            **kwargs,
            )
```
Get all cities in range 10km from city:
```python
    city = City.objects.all()[0]
    cities_in_range = city.in_range(10000)
```
How the sql query really looks like:
```python
{'sql': 'SELECT "app_city"."longitude", "app_city"."latitude", earth_box(ll_to_earth(51.03923, 16.97184), 10000) AS "earthbox" FROM "X" WHERE earth_box(ll_to_earth(51.03923, 16.97184), 10000) @> (ll_to_earth("X"."latitude", "X"."longitude")) LIMIT 21', 'time': '0.004'}

```
Requires **cube** and **earthdistance** extensions. To enable them you can:
```python
    operations = [
        CreateExtension("cube"),
        CreateExtension("earthdistance"),
        # you can also create an index like that:
        migrations.RunSQL(
            "CREATE INDEX indexname ON yourapp_yourmodel USING gist(ll_to_earth(latitude_column_name, longitude_column_name));"
        ),
    ]
```
or
```python
from django.db import connection

cursor = connection.cursor()
cursor.execute("CREATE EXTENSION cube;")
cursor.execute("CREATE EXTENSION earthdistance;")

```

How the functions looks like:
```python
def filter_in_range(
    queryset: QuerySet,
    latitude: float,
    longitude: float,
    range_in_meters: int,
    latitude_column_name: str = "latitude",
    longitude_column_name: str = "longitude",
    field_name: str = "earthbox",
    lookup_exp: str = "in_georange",
):
    earthbox = {field_name: EarthBox(LLToEarth(latitude, longitude), range_in_meters)}
    lookup = "%s__%s" % (field_name, lookup_exp)
    in_range = {lookup: LLToEarth(latitude_column_name, longitude_column_name)}
    return queryset.annotate(**earthbox).filter(**in_range)
```

Example model with **filter_in_range** function:
```python

class City(models.Model):
    longitude = models.FloatField(db_index=True)
    latitude = models.FloatField(db_index=True)

    def in_range(self, range_in_meters, **kwargs):
        return filter_in_range(
            self.__class__.objects,
            latitude=self.latitude,
            longitude=self.longitude,
            range_in_meters=range_in_meters,
            latitude_column_name="latitude",
            longitude_column_name="longitude",
            **kwargs,
        )
```

You need 2 extensions in postgres: **cube**, **earthdistance**, you can add that to your migrations:
```python
    operations = [
        CreateExtension("cube"),
        CreateExtension("earthdistance"),
        # you can also create an index like that:
        migrations.RunSQL(
            "CREATE INDEX indexname ON yourapp_yourmodel USING gist(ll_to_earth(latitude_column_name, longitude_column_name));"
        ),
    ]
```
or
```python
from django.db import connection

cursor = connection.cursor()
cursor.execute("CREATE EXTENSION cube;")
cursor.execute("CREATE EXTENSION earthdistance;")

```


data for map generation used from geonames.org
