from django.db.models import Lookup, Field, fields, Func, QuerySet


class LLToEarth(Func):
    function = "ll_to_earth"
    arg_joiner = ", "
    arity = 2  # The number of arguments the function accepts.

    def __init__(self, *expressions, output_field=None, **extra):
        if output_field is None:
            output_field = fields.Field()
        super().__init__(*expressions, output_field=output_field, **extra)


class EarthBox(LLToEarth):
    function = "earth_box"
    arg_joiner = ", "


@Field.register_lookup
class Near(Lookup):
    lookup_name = "in_georange"
    operator = "@>"

    def as_sql(self, compiler, connection):
        lhs, lhs_params = self.process_lhs(compiler, connection)
        rhs, rhs_params = self.process_rhs(compiler, connection)
        params = lhs_params + rhs_params
        return "%s @> %s" % (lhs, rhs), params


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
