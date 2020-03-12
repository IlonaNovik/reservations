from django.db import models


class Reservation(models.Model):
    number = models.CharField(max_length=100)
    arrival = models.DateField()
    departure = models.DateField()
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    no_of_people = models.IntegerField()
    status = models.CharField(max_length=100)
