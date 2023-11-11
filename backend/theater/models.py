from account.models import User
from django.contrib.gis.db import models
from common.models import BaseModel


# Create your models here.
class Theater(BaseModel):
    name = models.CharField(max_length=128)
    location = models.PointField()

    def __str__(self):
        return f"<Theater {self.name}>"


class Screen(BaseModel):
    name = models.CharField(max_length=16)
    theatre = models.ForeignKey(Theater, on_delete=models.CASCADE)
    no_of_rows = models.IntegerField(min=1)
    no_of_cols = models.IntegerField(min=1)

    def __str__(self):
        return f"<Screen {self.name} | {self.theatre.name}>"
