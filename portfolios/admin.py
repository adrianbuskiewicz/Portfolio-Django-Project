from django.contrib import admin
from .models import (
    Portfolio,
    CompanyWeight,
    MVP,
    ORP,
    BoughtPortfolio,
    BoughtCompaniesStocks,
)

# Register your models here.

admin.site.register(Portfolio)
admin.site.register(CompanyWeight)
admin.site.register(BoughtPortfolio)
admin.site.register(MVP)
admin.site.register(ORP)
admin.site.register(BoughtCompaniesStocks)
