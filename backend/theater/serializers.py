from rest_framework import serializers
from .models import Theater


class PointFieldSerializer(serializers.Serializer):
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()

    def to_representation(self, value):
        return {"latitude": value.y, "longitude": value.x}

    def to_internal_value(self, data):
        latitude = data.get('latitude')
        longitude = data.get('longitude')

        if latitude is None or longitude is None:
            raise serializers.ValidationError("Longitude and latitude fields must be included.")

        return Point(longitude, latitude)


class TheaterSerializer(serializers.ModelSerializer):
    location = PointFieldSerializer()

    class Meta:
        model = Theater
        fields = '__all__'

    def create(self, validated_data):
        return Theater.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.address = validated_data.get("address", instance.address)
        instance.short_address = validated_data.get("short_address", instance.short_address)
        instance.location = validated_data.get("location", instance.location)
        instance.zip_code = validated_data.get("zip_code", instance.zip_code)
        instance.technologies = validated_data.get("technologies", instance.technologies)
        instance.cuisines = validated_data.get("cuisines", instance.cuisines)
        instance.shows = validated_data.get("shows", instance.shows)
        instance.no_of_rows = validated_data.get("no_of_rows", instance.no_of_rows)
        instance.no_of_cols = validated_data.get("no_of_cols", instance.no_of_cols)
        instance.save()
        return instance


class TheaterOutputSerializer(TheaterSerializer):
    pass


class TheaterUpdateSerializer(TheaterSerializer):
    pass
