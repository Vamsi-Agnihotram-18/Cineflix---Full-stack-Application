from django.db import models
import uuid

class Show(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    movie = models.CharField(max_length=255)
    theatre = models.CharField(max_length=255)
    show_timings = models.JSONField(default=list)  # Assuming a list of strings
    runtime = models.CharField(max_length=10)
    remaining_seats = models.JSONField(default=list)  # Assuming a list of strings

    def __str__(self):
        return f"{self.movie} at {self.theatre} - {self.show_timings}"