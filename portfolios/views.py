from django.shortcuts import render, redirect, reverse
from companies.models import Company
from .forms import CalculatePortfoliosForm
from .models import MVP, ORP, BoughtPortfolio, CompanyWeight
from .utils_financial import mvp_calculate, orp_calculate


# Create your views here.


def calculate_portfolios_view(request):
    companies = Company.objects.filter(user=request.user).filter(used_in_portfolio='yes').order_by(
        'financialprofile__volatility',
        '-financialprofile__rate_of_return',
    )
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
    mvp_weights = mvp.company_weights.all() if mvp else None
    orp_weights = orp.company_weights.all() if orp else None
    start_date = companies[0].financialprofile.start_date
    end_date = companies[0].financialprofile.end_date

    if request.method == 'POST':
        calculate_portfolios_form = CalculatePortfoliosForm(request.POST)
        if calculate_portfolios_form.is_valid():
            rf = calculate_portfolios_form.cleaned_data.get('rf')
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
            mvp.company_weights.all().delete()
            orp.company_weights.all().delete()
            for symbol, weight in mvp_portfolio['companies_weights'].items():
                company_weight = CompanyWeight(company=companies.get(symbol=symbol), company_weight=weight)
                company_weight.save()
                mvp.company_weights.add(company_weight)
            for symbol, weight in orp_portfolio['companies_weights'].items():
                company_weight = CompanyWeight(company=companies.get(symbol=symbol), company_weight=weight)
                company_weight.save()
                orp.company_weights.add(company_weight)
        return redirect(reverse('portfolios:create_portfolios'))
    else:
        calculate_portfolios_form = CalculatePortfoliosForm()

    context = {
        'companies': companies,
        'calculate_portfolios_form': calculate_portfolios_form,
        'start_date':  start_date.strftime('%d.%m.%Y'),
        'end_date':  end_date.strftime('%d.%m.%Y'),
        'mvp': mvp,
        'mvp_weights': mvp_weights,
        'orp': orp,
        'orp_weights': orp_weights,
    }

    return render(request, 'portfolios/portfolios.html', context=context)
