from django.urls import path
from .views import home_view, delete_company_view, edit_company_view, use_company_view

app_name = 'companies'

urlpatterns = [
    path('', home_view, name='home'),
    path('delete/<pk>/', delete_company_view, name='company_delete'),
    path('edit/<pk>/', edit_company_view, name='company_edit'),
    path('use/<pk>/', use_company_view, name='company_use'),
]