from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from account.models import Token, User
from reservation.models import Ticket
from django.utils import timezone
from account.serializers import CustomSignUpSerializer, CustomLoginSerializer, CustomUserSerializer
from account.auth import CustomAPIAccessAuthentication
from theater.serializers import CustomTheaterOutputSerializer
from movie.serializers import CustomMovieSerializer
from datetime import datetime, timedelta
from theater.models import Cinema, Screening
from movie.serializers import FilmSerializer
from reservation.models import Reservation

class CustomUserRegistrationAPI(APIView):
    SerializerClass = CustomSignUpSerializer

    def post(self, request):
        data = request.data
        user_data = data

        if "password" not in data:
            user_data = {
                "email": data["email"],
                "phoneNumber": data["phoneNumber"],
                "username": data["username"],
                "role": User.GUEST_USER,
                "rewardPoints": 0,
                "is_admin": False,
                "password": "customGuestUser123",
                "confirm_password": "customGuestUser123",
            }

        serializer = self.SerializerClass(data=user_data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        Token.objects.get_or_create(user=user)

        response_data = {
            "success": True,
            "id": user.id,
            "token": CustomAPIAccessAuthentication.generate_jwt_token(user),
            "email": user.email,
            "role": user.role,
            "username": user.username,
            "phoneNumber": str(user.phoneNumber),
            "is_admin": user.is_admin,
            **CustomUserSerializer(instance=user).data,
        }

        return Response(response_data, status=status.HTTP_201_CREATED)


class CustomUserLoginAPI(APIView):
    SerializerClass = CustomLoginSerializer

    def post(self, request):
        serializer = self.SerializerClass(data=request.data)
        serializer.is_valid(raise_exception=True)

        response_data = {
            "success": True,
            "id": serializer.validated_data["user"].id,
            "token": CustomAPIAccessAuthentication.generate_jwt_token(serializer.validated_data["user"]),
            "email": serializer.validated_data["user"].email,
            "role": serializer.validated_data["user"].role,
            "username": serializer.validated_data["user"].username,
            "phoneNumber": str(serializer.validated_data["user"].phoneNumber),
            "is_admin": serializer.validated_data["user"].is_admin,
            **(CustomUserSerializer(instance=serializer.validated_data["user"]).data),
        }

        return Response(response_data, status=status.HTTP_200_OK)


class CustomUserDetailsAPI(APIView):
    def get(self, request, id):
        try:
            user = User.objects.get(id=id)
        except User.DoesNotExist:
            return Response({'error': 'Invalid User ID'}, status=status.HTTP_404_NOT_FOUND)

        thirty_days_ago = timezone.now() - timezone.timedelta(days=30)
        tickets = Ticket.objects.filter(user=user).filter(created_at__gte=thirty_days_ago).filter(
            created_at__lte=timezone.now()).select_related('show')
        tickets_data = TicketSerializer(tickets, many=True).data

        for i, ticket in enumerate(tickets):
            show_data = {
                "id": ticket.show.id,
                "show_timing": ticket.show.show_timing,
                "runtime": ticket.show.movie.runtime
            }

            tickets_data[i]["theater"] = CustomTheaterOutputSerializer(ticket.show.theater).data
            tickets_data[i]["movie"] = CustomMovieSerializer(ticket.show.movie).data
            tickets_data[i]["show"] = show_data

        response_data = {
            "user": CustomUserSerializer(user).data,
            "tickets": tickets_data,
        }

        return Response(response_data, status=status.HTTP_200_OK)

    def patch(self, request, id):
        data = request.data

        try:
            user = User.objects.get(id=id)
        except User.DoesNotExist:
            return Response({'error': 'Invalid User ID'}, status=status.HTTP_404_NOT_FOUND)

        user.membership_type = data.get("membership_type", user.membership_type)
        user.save()

        response_data = {
            "success": True,
            "id": user.id,
            "token": CustomAPIAccessAuthentication.generate_jwt_token(user),
            "email": user.email,
            "role": user.role,
            "username": user.username,
            "phoneNumber": str(user.phoneNumber),
            "is_admin": user.is_admin,
            **(CustomUserSerializer(instance=user).data),
        }

        return Response(response_data, status=status.HTTP_200_OK)


class CinemaOccupancyView(APIView):
    def calculate_occupancy(self, cinemas, start_date, end_date):
        occupancy = {}
        for cinema in cinemas:
            screenings = Screening.objects.filter(cinema=cinema)
            for reservation in Reservation.objects.filter(screening__in=screenings, screening__start_time__gte=start_date, screening__start_time__lte=end_date):
                occupancy.setdefault(cinema.zip_code, 0)
                occupancy[cinema.zip_code] += len(reservation.seats)
        return occupancy

    def get(self, request):
        today = timezone.now()
        last_30_days = today - timedelta(days=30)
        last_60_days = today - timedelta(days=60)
        last_90_days = today - timedelta(days=90)

        cinemas = Cinema.objects.all()

        locations_30_days = self.calculate_occupancy(cinemas, last_30_days, today)
        locations_60_days = self.calculate_occupancy(cinemas, last_60_days, today)
        locations_90_days = self.calculate_occupancy(cinemas, last_90_days, today)

        films_30_days = self.calculate_film_occupancy(last_30_days, today)
        films_60_days = self.calculate_film_occupancy(last_60_days, today)
        films_90_days = self.calculate_film_occupancy(last_90_days, today)

        return Response({
            "locations_30_days": locations_30_days,
            "locations_60_days": locations_60_days,
            "locations_90_days": locations_90_days,
            "films_30_days": films_30_days,
            "films_60_days": films_60_days,
            "films_90_days": films_90_days
        }, status=status.HTTP_200_OK)

    def calculate_film_occupancy(self, start_date, end_date):
        film_occupancy = {}
        for reservation in Reservation.objects.filter(screening__start_time__gte=start_date, screening__start_time__lte=end_date):
            film = reservation.screening.film
            serializer = FilmSerializer(film)
            film_data = serializer.data
            film_data["status"] = "Upcoming" if datetime.strptime(film_data["release_date"], "%Y-%m-%d").date() > timezone.now().date() else "Now Showing"
            film_data["occupancy"] = film_occupancy.get(film.id, 0) + len(reservation.seats)
            film_occupancy[film.id] = film_data
        return film_occupancy
