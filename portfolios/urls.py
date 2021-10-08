from django.urls import path
from .views import (
    calculate_portfolios_view,
    not_use_company_view,
    BoughtPortfolios,
    BoughtPortfolioDetail,
    create_bought_portfolio_view,
    delete_bought_portfolio_view,
)


app_name = 'portfolios'

urlpatterns = [
    path('', calculate_portfolios_view, name='create_portfolios'),
    path('not-use-company/<pk>/', not_use_company_view, name='not_use_company'),
    path('bought-portfolios/', BoughtPortfolios.as_view(), name='bought_portfolios'),
    path('bought-portfolios/<pk>/', BoughtPortfolioDetail.as_view(), name='bought_portfolio_info'),
    path('bought-portfolios/create-bought-portfolio/<pk>/', create_bought_portfolio_view, name='create_bought_portfolio'),
    path('bought-portfolios/delete/<pk>/', delete_bought_portfolio_view, name='delete_bought_portfolio'),
]
