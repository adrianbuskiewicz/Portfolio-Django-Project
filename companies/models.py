from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Company(models.Model):
    symbol = models.CharField(max_length=5)
    name = models.CharField(max_length=100)
    rate_of_return = models.FloatField(null=True, blank=True)
    volatility = models.FloatField(null=True, blank=True)
    user = models.ManyToManyField(User)

    def __str__(self):
        return str(self.name)

