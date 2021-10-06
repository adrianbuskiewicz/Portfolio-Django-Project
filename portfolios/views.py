from django.shortcuts import render, redirect, reverse, get_object_or_404
from companies.models import Company
from .forms import CalculatePortfoliosForm, BoughtPortfolioForm
from .models import MVP, ORP, BoughtPortfolio, CompanyWeight, BoughtCompaniesStocks, Portfolio
from .utils_financial import mvp_calculate, orp_calculate, get_actual_price, calculate_stocks_amount
from django.views.generic import ListView, DetailView
from django.contrib import messages
from datetime import datetime as dt


# Create your views here.


def calculate_portfolios_view(request):
    # We want just user companies to display and use them in MVP and ORP
    companies = Company.objects.filter(user=request.user).filter(used_in_portfolio='yes').order_by(
        'financialprofile__volatility',
        '-financialprofile__rate_of_return',
    )
    # We are looking for user's MVP and ORP (create them if are not in db)
    mvp, created = MVP.objects.get_or_create(
        user=request.user,
        defaults={'rate_of_return': None,
                  'volatility': None,
                  'portfolio_type': 'mvp',
                  'user': request.user,
                  }
    )
    orp, created = ORP.objects.get_or_create(
        user=request.user,
        defaults={'rate_of_return': None,
                  'volatility': None,
                  'portfolio_type': 'orp',
                  'user': request.user,
                  'rf': 0,
                  }
    )
    # Dates between we calculated our rates and volatility for our companies
    start_date = companies[0].financialprofile.start_date if companies else None
    end_date = companies[0].financialprofile.end_date if companies else None

    if request.method == 'POST':
        calculate_portfolios_form = CalculatePortfoliosForm(request.POST)
        invest_portfolio_form = BoughtPortfolioForm(request.POST)
        if calculate_portfolios_form.is_valid():
            rf = calculate_portfolios_form.cleaned_data.get('rf')
            # We are calculating MVP and ORP with our financial functions
            mvp_portfolio = mvp_calculate(
                companies=companies,
                start=start_date,
                end=end_date,
            )
            orp_portfolio = orp_calculate(
                companies=companies,
                start=start_date,
                end=end_date,
                rf=rf,
            )
            mvp, created = MVP.objects.update_or_create(
                user=request.user,
                defaults={'rate_of_return': mvp_portfolio['rate_of_return'],
                          'volatility': mvp_portfolio['volatility'],
                          'portfolio_type': 'mvp',
                          'user': request.user,
                          }
            )
            orp, created = ORP.objects.update_or_create(
                user=request.user,
                defaults={'rate_of_return': orp_portfolio['rate_of_return'],
                          'volatility': orp_portfolio['volatility'],
                          'portfolio_type': 'orp',
                          'user': request.user,
                          'rf': rf,
                          }
            )
            # Deleting previous company weights because we want to replace them with new ones
            mvp.company_weights.all().delete()
            orp.company_weights.all().delete()
            # Adding our companies weights to portfolios (many to many)
            for symbol, weight in mvp_portfolio['companies_weights'].items():
                company_weight = CompanyWeight(company=companies.get(symbol=symbol), company_weight=weight)
                company_weight.save()
                mvp.company_weights.add(company_weight)
            for symbol, weight in orp_portfolio['companies_weights'].items():
                company_weight = CompanyWeight(company=companies.get(symbol=symbol), company_weight=weight)
                company_weight.save()
                orp.company_weights.add(company_weight)
            messages.success(request, "MVP and ORP created!")
        return redirect(reverse('portfolios:create_portfolios'))

    else:
        calculate_portfolios_form = CalculatePortfoliosForm()
        invest_portfolio_form = BoughtPortfolioForm()

    context = {
        'companies': companies,
        'calculate_portfolios_form': calculate_portfolios_form,
        'start_date':  start_date.strftime('%d.%m.%Y') if companies else None,
        'end_date':  end_date.strftime('%d.%m.%Y') if companies else None,
        'mvp': mvp,
        'orp': orp,
        'invest_portfolio_form': invest_portfolio_form,
    }

    return render(request, 'portfolios/portfolios.html', context=context)


def not_use_company_view(request, pk):
    # Changing used company to not used and redirecting to same page
    company_to_use = get_object_or_404(Company, pk=pk)
    if request.method == 'POST':
        if company_to_use.used_in_portfolio == 'yes':
            company_to_use.used_in_portfolio = 'no'
            company_to_use.save()
    return redirect(reverse('portfolios:create_portfolios'))


def create_bought_portfolio_view(request, pk):
    portfolio = get_object_or_404(Portfolio, pk=pk)
    if portfolio.portfolio_type == 'mvp':
        portfolio = get_object_or_404(MVP, pk=pk)
    elif portfolio.portfolio_type == 'orp':
        portfolio = get_object_or_404(ORP, pk=pk)
    if request.method == 'POST':
        invest_portfolio_form = BoughtPortfolioForm(request.POST or None)
        if invest_portfolio_form.is_valid():
            budget = invest_portfolio_form.cleaned_data['budget']
            new_bought_portfolio = BoughtPortfolio.objects.create(
                user=request.user,
                budget=budget,
                purchase_date=dt.now(),
                rate_of_return=portfolio.rate_of_return,
                volatility=portfolio.volatility,
                portfolio_type=portfolio.portfolio_type.upper(),
            )
            new_bought_portfolio.save()
            for company_weight in portfolio.company_weights.all():
                actual_price = get_actual_price(company_weight.company.symbol)
                stocks_amount = calculate_stocks_amount(
                        budget=budget,
                        weight=company_weight.company_weight,
                        symbol=company_weight.company.symbol,
                    )
                stocks = BoughtCompaniesStocks(
                    symbol=company_weight.company.symbol,
                    name=company_weight.company.name,
                    weight=company_weight.company_weight,
                    predicted_rate_of_return=company_weight.company.financialprofile.rate_of_return,
                    predicted_volatility=company_weight.company.financialprofile.volatility,
                    purchase_price=actual_price['price'],
                    owned_stocks_amount=stocks_amount,
                    owned_capital=actual_price['price']*stocks_amount,
                    date_of_purchase=actual_price['date'],
                    bought_portfolio=new_bought_portfolio,
                )
                stocks.save()
    return redirect(reverse('portfolios:create_portfolios'))


class BoughtPortfolios(ListView):
    model = BoughtPortfolio
    template_name = 'portfolios/bought_portfolios.html'
    context_object_name = 'bought_portfolios'
    paginate_by = 6

    def get_queryset(self):
        return BoughtPortfolio.objects.filter(user=self.request.user).order_by(
                'purchase_date',
        )


class BoughtPortfolioDetail(DetailView):
    model = BoughtPortfolio
    template_name = 'portfolios/bought_portfolio_detail.html'
    context_object_name = 'bought_portfolio'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        stocks = BoughtCompaniesStocks.objects.filter(bought_portfolio=self.object.id)
        context['all_stocks'] = stocks
        return context






