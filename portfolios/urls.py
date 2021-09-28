from django.urls import path
from .views import calculate_portfolios_view

app_name = 'portfolios'

urlpatterns = [
    path('portfolios/', calculate_portfolios_view, name='create_portfolios'),
]
