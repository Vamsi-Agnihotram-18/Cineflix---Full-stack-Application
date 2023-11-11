from rest_framework import serializers

from rest_framework import serializers
from theater.models import Theater, Screen
from theater.selectors import theater_get
from core.errors import MissingResource

from django.contrib.gis.geos import Point
from .models import Theater


class PointFieldSerializer(serializers.Field):
    def to_representation(self, value):
        return {"latitude": value.y, "longitude": value.x}

    def to_internal_value(self, data):
        return Point(float(data["longitude"]), float(data["latitude"]))


class TheaterSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=128)
    location = PointFieldSerializer()


class ScreenSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=16)
    theatre = serializers.IntegerField()
    no_of_rows = serializers.IntegerField(min=1)
    no_of_cols = serializers.IntegerField(min=1)

    def validate(self, attrs):
        attrs = super().validate(attrs)
        theater_id = attrs["theater"]
        theater = theater_get(id=theater_id)
        if not theater:
            raise MissingResource(f"Theater {theater_id} not found")
        attrs["theater"] = theater
        return attrs
