from django.db import models
from companies.models import Company
from django.contrib.auth.models import User


# Create your models here.

class CompanyWeight(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    company_weight = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f'{self.company} - {self.company_weight:.2f}%'


class Portfolio(models.Model):
    rate_of_return = models.FloatField(null=True, blank=True)
    volatility = models.FloatField(null=True, blank=True)
    company_weights = models.ManyToManyField(CompanyWeight)
    PORTFOLIO_TYPES = [
        ('MVP', 'Minimal Volatility Portfolio'),
        ('ORP', 'Optimal Risky Portfolio'),
    ]
    portfolio_type = models.CharField(
        max_length=3,
        choices=PORTFOLIO_TYPES,
    )

    def __str__(self):
        return f'Id: {self.id} RoR: {self.rate_of_return:.2f}% - Vol: {self.volatility:.2f}%'


class MVP(Portfolio):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class ORP(Portfolio):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rf = models.FloatField(default=1)


class BoughtPortfolio(Portfolio):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    budget = models.FloatField(default=100000)


