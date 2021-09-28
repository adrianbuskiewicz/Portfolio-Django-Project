from django.db import models
from django.contrib.auth.models import User
from math import sqrt

# Create your models here.


class Company(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    symbol = models.CharField(
        max_length=10,
        unique=True,
        error_messages={'unique': 'This company is already added!'}
    )
    name = models.CharField(max_length=100)

    USED_STATUS = [
        ('yes', 'used'),
        ('no', 'not used'),
    ]
    used_in_portfolio = models.CharField(
        max_length=3,
        choices=USED_STATUS,
        default='no',
    )

    def __str__(self):
        return str(self.symbol)

    class Meta:
        verbose_name_plural = "Companies"


class FinancialProfile(models.Model):
    company = models.OneToOneField(Company, on_delete=models.CASCADE)
    rate_of_return = models.FloatField(null=True, blank=True)
    volatility = models.FloatField(null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    def annual_rate_of_return(self):
        ann_ror = self.rate_of_return * 250 if self.rate_of_return else None
        return round(ann_ror, 2)

    def annual_volatility(self):
        ann_vol = sqrt(self.volatility * 250) if self.rate_of_return else None
        return round(ann_vol, 2)

    def __str__(self):
        return f'{self.company} - RoR: ({self.rate_of_return}) - Vol: ({self.volatility})'
