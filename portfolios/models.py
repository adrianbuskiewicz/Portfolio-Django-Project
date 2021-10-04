from django.db import models
from companies.models import Company
from django.contrib.auth.models import User
from django.shortcuts import reverse
from .utils_financial import get_actual_price


# Create your models here.

class CompanyWeight(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    company_weight = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f'{self.company} - {self.company_weight:.2f}%'


class Portfolio(models.Model):
    rate_of_return = models.FloatField(null=True, blank=True)
    volatility = models.FloatField(null=True, blank=True)
    PORTFOLIO_TYPES = [
        ('MVP', 'Minimal Volatility Portfolio'),
        ('ORP', 'Optimal Risky Portfolio'),
    ]
    portfolio_type = models.CharField(
        max_length=3,
        choices=PORTFOLIO_TYPES,
    )

    def __str__(self):
        if (self.rate_of_return != None) and (self.volatility != None):
            return f'Id: {self.id} RoR: {self.rate_of_return:.2f}% - Vol: {self.volatility:.2f}%'
        else:
            return f'Id: {self.id}'


class MVP(Portfolio):
    # Every user will have one MVP which will be updated when using prediction form
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_weights = models.ManyToManyField(CompanyWeight)


class ORP(Portfolio):
    # Every user will have one ORP which will be updated when using prediction form
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_weights = models.ManyToManyField(CompanyWeight)
    rf = models.FloatField(default=1)


class BoughtPortfolio(Portfolio):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    budget = models.FloatField()
    purchase_date = models.DateTimeField()

    def get_absolute_url(self):
        return reverse('portfolios:bought_portfolio_info', args=[str(self.id)])

    def purchase_whole_owned_capital(self):
        return sum([stocks.owned_capital for stocks in BoughtCompaniesStocks.objects.filter(bought_portfolio=self)])

    def now_whole_owned_capital(self):
        return sum([stocks.actual_price() * stocks.owned_stocks_amount for stocks in BoughtCompaniesStocks.objects.filter(bought_portfolio=self)])

    def summary_return(self):
        return sum([stocks.single_return() for stocks in BoughtCompaniesStocks.objects.filter(bought_portfolio=self)])


class BoughtCompaniesStocks(models.Model):
    # Not using foreign key, due to let user delete companies in home page (just saving symbol and name)
    symbol = models.CharField(
        max_length=10,
    )
    name = models.CharField(max_length=100)
    weight = models.FloatField()
    predicted_rate_of_return = models.FloatField()
    predicted_volatility = models.FloatField()
    purchase_price = models.FloatField()
    owned_stocks_amount = models.IntegerField()
    owned_capital = models.FloatField()
    date_of_purchase = models.DateField()
    bought_portfolio = models.ForeignKey(BoughtPortfolio, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.symbol} - {self.purchase_price} - {self.owned_stocks_amount} - {self.date_of_purchase}'

    def actual_price(self):
        actual_price = get_actual_price(self.symbol)['price']
        return actual_price

    def price_difference(self):
        return self.actual_price() - self.purchase_price

    def single_return(self):
        return (self.actual_price() * self.owned_stocks_amount) - self.owned_capital

    class Meta:
        verbose_name_plural = "Bought companies stocks"
