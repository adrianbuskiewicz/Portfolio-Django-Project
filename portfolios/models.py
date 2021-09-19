from django.db import models
from companies.models import Company

# Create your models here.


class Portfolio(models.Model):
    rate_of_return = models.FloatField(null=True, blank=True)
    volatility = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"""
        Id: {self.id} 
        RoR: {self.rate_of_return:.2f}% - Vol: {self.volatility:.2f}%
        """


class CompanyWeight(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    company_weight = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f'{self.portfolio} - {self.company} - {self.company_weight:.2f}%'