from django.contrib import admin
from .models import Company, FinancialProfile

# Register your models here.

admin.site.register(Company)
admin.site.register(FinancialProfile)
