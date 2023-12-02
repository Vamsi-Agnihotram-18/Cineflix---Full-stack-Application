from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime, timedelta, time
from .models import Show, Movie, Theater
from movie.serializers import MovieSerializer
from theater.serializers import TheaterOutputSerializer
import pytz

class CreateShowsView(APIView):
    def post(self, request, format=None):
        data = request.data
        movie_id = data.get('movie_id')
        theater_id_list = data.get('theater_id_list')
        start_date = datetime.fromisoformat(data.get('start_date'))
        end_date = datetime.fromisoformat(data.get('end_date'))
        price = data.get("price", 10)
        discounted_price = data.get("discounted_price", price)

        if not all([movie_id, theater_id_list, start_date, end_date]):
            return Response({'error': 'Missing required fields'}, status=status.HTTP_400_BAD_REQUEST)

        date_range = [start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1)]
        shows = []
        for show_date in date_range:
            for theater_id in theater_id_list:
                try:
                    theater = Theater.objects.get(id=theater_id)
                    movie = Movie.objects.get(id=movie_id)
                    for show_time in theater.shows.all():
                        show_datetime = show_date.replace(
                            hour=show_time.show_timing.hour,
                            minute=show_time.show_timing.minute,
                            second=0,
                            microsecond=0
                        )
                        pst = pytz.timezone('America/Los_Angeles')
                        show_datetime = pst.localize(show_datetime)
                        shows.append(Show.objects.create(
                            movie=movie,
                            theater=theater,
                            show_timing=show_datetime,
                            seat_matrix=[],
                            no_of_rows=theater.no_of_rows,
                            no_of_cols=theater.no_of_cols,
                            price=price,
                            discounted_price=discounted_price
                        ).id)
                except (Movie.DoesNotExist, Theater.DoesNotExist):
                    return Response({'error': 'Movie or Theater with provided ID not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'message': 'Shows created successfully', "shows": shows}, status=status.HTTP_201_CREATED)

class ShowGetDeleteAPI(APIView):
    def get(self, request, id, format=None):
        try:
            show = Show.objects.get(id=id)
            discounted_price = show.discounted_price if show.show_timing.weekday() == 1 or show.show_timing.time() < time(18, 00) else show.price
            response_data = {
                "id": show.id,
                "show_timing": show.show_timing,
                "no_of_rows": show.no_of_rows,
                "no_of_cols": show.no_of_cols,
                "price": show.price,
                "discounted_price": discounted_price,
                "movie": MovieSerializer(show.movie).data,
                "theater": TheaterOutputSerializer(show.theater).data,
                "seat_matrix": show.seat_matrix,
                "runtime": show.movie.runtime if hasattr(show.movie, 'runtime') else None
            }
            return Response({"show": response_data})
        except Show.DoesNotExist:
            return Response({'error': 'Show not found'}, status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, id):
        try:
            show = Show.objects.get(id=id)
            show.delete()
            return Response({'message': 'Show deleted successfully'})
        except Show.DoesNotExist:
            return Response({'message': 'Show not found'}, status=status.HTTP_404_NOT_FOUND)

class ShowsGetByMovieAPI(APIView):
    def get(self, request, movie_id):
        try:
            movie = Movie.objects.get(id=movie_id)
        except Movie.DoesNotExist:
            return Response({'error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)
        
        date_str = request.query_params.get("date", datetime.now().date())
        date = datetime.strptime(date_str, "%Y-%m-%d")
        
        shows = Show.objects.filter(movie_id=movie_id, show_timing__date=date).select_related('theater').order_by('show_timing')

        theaters_with_shows = {}
        for show in shows:
            theater_id = show.theater.id

            if theater_id not in theaters_with_shows:
                theaters_with_shows[theater_id] = {
                    'theater': TheaterOutputSerializer(show.theater).data,
                    'shows': []
                }

            theaters_with_shows[theater_id]['shows'].append({
                'id': show.id,
                'show_timing': show.show_timing,
            })

        theaters_with_shows_list = list(theaters_with_shows.values())
        return Response({"movie": MovieSerializer(movie).data, "theaters": theaters_with_shows_list})

class MoviesGetByTheaterAPI(APIView):
    def get(self, request, theater_id):
        try:
            theater = Theater.objects.get(id=theater_id)
        except Theater.DoesNotExist:
            return Response({'error': 'Theater not found'}, status=status.HTTP_404_NOT_FOUND)
        
        date_str = request.query_params.get("date", datetime.now().date())
        date = datetime.strptime(date_str, "%Y-%m-%d")
        
        shows = Show.objects.filter(theater_id=theater_id, show_timing__date=date).select_related('movie').order_by('show_timing')

        movie_with_shows = {}
        for show in shows:
            movie_id = show.movie
