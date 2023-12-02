from django.db import models
from theater.models import Cinema
from movie.models import Film
from shows.models import Screening
from account.models import CustomUser
from common.models import BaseModel

class Reservation(BaseModel):
    CONFIRMED = 'confirmed'
    CANCELLED = 'cancelled'
    STATUS_CHOICES = [(CONFIRMED, 'Confirmed'), (CANCELLED, 'Cancelled')]
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    screening = models.ForeignKey(Screening, on_delete=models.CASCADE)
    ticket_price = models.FloatField(blank=True, null=True)
    service_fee = models.FloatField(blank=True, null=True)
    seats = models.JSONField(default=list)
    status = models.CharField(choices=STATUS_CHOICES, default=CONFIRMED, max_length=20)
    dollars = models.FloatField(blank=True, null=True)
    reward_points = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.id} - {self.screening} - {self.ticket_price}"
