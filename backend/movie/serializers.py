from rest_framework import serializers
from .models import Movie

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['id', 'name', 'runtime', 'genre', 'rating', 'description', 'image_url', 'start_date']

    def create(self, validated_data):
        movie = Movie.objects.create(**validated_data)
        return movie

class MovieUpdateSerializer(MovieSerializer):
    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.runtime = validated_data.get("runtime", instance.runtime)
        instance.genre = validated_data.get("genre", instance.genre)
        instance.rating = validated_data.get("rating", instance.rating)
        instance.description = validated_data.get("description", instance.description)
        instance.image_url = validated_data.get("image_url", instance.image_url)
        instance.start_date = validated_data.get("start_date", instance.start_date)
        instance.save()
        return instance

class MovieFilterSerializer(serializers.Serializer):
    sort_by = serializers.ChoiceField(choices=['recent', 'popular', 'alphabetical'], required=False)
    genre = serializers.ChoiceField(choices=['thriller', 'horror', 'rom_com', 'feel_good', 'action'], required=False)
    rating = serializers.IntegerField(required=False)
