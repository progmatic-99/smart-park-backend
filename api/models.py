from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    __tablename__ = "users"

    name = models.CharField(max_length=100)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255, null=False)

    REQUIRED_FIELDS = ["email", "password"]


class Booking(models.Model):
    __tablename__ = "bookings"

    slot_number = models.IntegerField()
    cost = models.IntegerField()
    time = models.DateTimeField()
    duration = models.DurationField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
