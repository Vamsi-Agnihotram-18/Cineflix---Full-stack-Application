from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from theater.models import Theater
from core.mixins import ApiAuthenticationMixin
from core.errors import MissingResource
from theater.services import theater_create
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import random

class TheaterListCreateAPI(APIView):
    Serializer = TheaterSerializer

    def post(self, request):
        data = request.data
        try:
            geolocator = Nominatim(user_agent=f"User agent: {random.randint(1, 10000)}")
            location = geolocator.geocode(data["address"])
            data["location"] = {
                "latitude": location.latitude,
                "longitude": location.longitude
            }
            data["zip_code"] = location.raw['display_name'].split(",")[-2]
        except:
            data["location"] = {
                "latitude": 37.3405074,
                "longitude": -121.89838687255096
            }
            data["zip_code"] = "95110"
        
        serializer = self.Serializer(data=data)
        serializer.is_valid(raise_exception=True)
        theater = serializer.save()
        return Response({"theater": self.Serializer(instance=theater).data}, status=status.HTTP_201_CREATED)
    
    def get(self, request):
        query_params = request.query_params
        latitude = query_params.get("latitude")
        longitude = query_params.get("longitude")
        zip_code = query_params.get("zip_code")
        theaters = Theater.objects.all()

        if zip_code:
            theaters = theaters.filter(zip_code=zip_code)

        theaters_data = []
        for theater in theaters:
            theater_data = self.Serializer(instance=theater).data

            if latitude and longitude:
                distance = geodesic(
                    (theater.location.y, theater.location.x), (float(latitude), float(longitude))
                ).miles
            elif zip_code:
                try:
                    geolocator = Nominatim(user_agent=f"User agent: {random.randint(1, 10000)}")
                    location = geolocator.geocode(f"{zip_code}, USA")
                    coordinates = (location.latitude, location.longitude)
                    distance = geodesic(coordinates, (theater.location.y, theater.location.x)).miles
                    if distance > 20:
                        continue
                except:
                    distance = 1.5
            else:
                distance = 1.2

            theater_data["distance"] = round(distance, 1)
            theaters_data.append(theater_data)

        return Response({"theaters": theaters_data}, status=status.HTTP_200_OK)


class TheaterGetUpdateDeleteAPI(APIView):
    Serializer = TheaterSerializer
    
    def get(self, request, pk):
        try:
            theater = Theater.objects.get(id=pk)
            serializer = self.Serializer(instance=theater)
            return Response(serializer.data)
        except Theater.DoesNotExist:
            return Response({'message': 'Theater not found'}, status=status.HTTP_404_NOT_FOUND)
    
    def patch(self, request, pk):
        try:
            theater = Theater.objects.get(id=pk)
        except Theater.DoesNotExist:
            return Response({'message': 'Theater not found'}, status=status.HTTP_404_NOT_FOUND)
        
        data = request.data
        try:
            geolocator = Nominatim(user_agent=f"User agent: {random.randint(1, 10000)}")
            location = geolocator.geocode(data["address"])
            data["location"] = {
                "latitude": location.latitude,
                "longitude": location.longitude
            }
            data["zip_code"] = location.raw['display_name'].split(",")[-2]
        except:
            data["location"] = {
                "latitude": 37.3405074,
                "longitude": -121.89838687255096
            }
            data["zip_code"] = "95110"
        
        serializer = self.Serializer(instance=theater, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'theater': serializer.data}, status=status.HTTP_200_OK)
    
    def delete(self, request, pk):
        try:
            theater = Theater.objects.get(id=pk)
            theater.delete()
            return Response({'message': 'Theater deleted successfully'})
        except Theater.DoesNotExist:
            return Response({'message': 'Theater not found'}, status=status.HTTP_404_NOT_FOUND)
