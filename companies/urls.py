from django.urls import path
from .views import (
    home_view,
    create_company_view,
    delete_company_view,
    edit_company_view,
    use_company_view,
    calculate_stats_view,
)

app_name = 'companies'

urlpatterns = [
    path('', home_view, name='home'),
    path('companies/create/', create_company_view, name='create_company'),
    path('companies/delete/<pk>/', delete_company_view, name='delete_company'),
    path('companies/edit/<pk>/', edit_company_view, name='edit_company'),
    path('companies/use/<pk>/', use_company_view, name='use_company'),
    path('companies/calculate-stats/', calculate_stats_view, name='calculate_stats'),
]