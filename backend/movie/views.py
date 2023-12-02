from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from datetime import datetime
from .models import Movie
from .serializers import (
    MovieSerializer,
    MovieUpdateSerializer,
    MovieFilterSerializer
)

class MovieGetUpdateDeleteAPI(APIView):
    def get(self, request, pk):
        try:
            movie = Movie.objects.get(id=pk)
            serializer = MovieSerializer(movie)
            movie_data = serializer.data
            start_date = datetime.strptime(movie_data["start_date"], "%Y-%m-%d").date()
            movie_data["type"] = "Upcoming" if start_date > timezone.now().date() else "Playing Now"
            return Response({"movie": movie_data}, status=status.HTTP_200_OK)
        except Movie.DoesNotExist:
            return Response({'message': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)
    
    def patch(self, request, pk):
        try:
            movie = Movie.objects.get(id=pk)
            serializer = MovieUpdateSerializer(movie, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'movie': serializer.data}, status=status.HTTP_200_OK)
        except Movie.DoesNotExist:
            return Response({'message': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            movie = Movie.objects.get(id=pk)
            movie.delete()
            return Response({'message': 'Movie deleted successfully'})
        except Movie.DoesNotExist:
            return Response({'message': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)

class MovieListCreateAPI(APIView):
    def get(self, request):
        movies = Movie.objects.all()
        query_params = request.query_params
        serializer = MovieFilterSerializer(data=query_params)
        serializer.is_valid(raise_exception=True)
        filters = serializer.validated_data

        if "genre" in filters:
            movies = movies.filter(genre=filters["genre"])
        if "rating" in filters:
            movies = movies.filter(rating__gte=filters["rating"])
        if "sort_by" in filters:
            if filters["sort_by"] == "recent":
                movies = movies.order_by('start_date')
            elif filters["sort_by"] == "popular":
                movies = movies.order_by('-rating')
            elif filters["sort_by"] == "alphabetical":
                movies = movies.order_by('name')

        serializer = MovieSerializer(movies, many=True)
        movies_data = serializer.data

        for movie in movies_data:
            start_date = datetime.strptime(movie["start_date"], "%Y-%m-%d").date()
            movie["type"] = "Upcoming" if start_date > timezone.now().date() else "Playing Now"

        return Response({"movies": movies_data}, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = MovieSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"movie": serializer.data}, status=status.HTTP_201_CREATED)
