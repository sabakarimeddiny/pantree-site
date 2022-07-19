from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ings = models.CharField(max_length=10000)