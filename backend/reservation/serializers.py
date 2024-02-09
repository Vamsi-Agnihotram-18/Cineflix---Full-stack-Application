from rest_framework import serializers
from reservation.models import Reservation

class ReservationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reservation
        fields = ['id', 'screening', 'user', 'ticket_price', 'service_fee', 'seats', 'dollars', 'reward_points', 'status', 'created_at']

    def create(self, validated_data):
        reservation = Reservation.objects.create(**validated_data)
        return reservation
