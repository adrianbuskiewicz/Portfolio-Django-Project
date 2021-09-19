from django.shortcuts import render
from .models import Company
from .utils_financial import company_df, df_mean_price, df_vol_price
from .forms import CompanyForm

# Create your views here.


def home_view(request):
    companies = Company.objects.all()
    symbols = [company.symbol for company in companies]
    df = company_df(symbols)
    df = df.to_html()
    stats = []
    for company in companies:
        stats.append({
            'name': company.name,
            'symbol': company.symbol,
            'price_mean': round(df_mean_price(company.symbol), 2),
            'price_vol': round(df_vol_price(company.symbol), 2),
        })

    form = CompanyForm()
    if request.method == 'POST':
        company = Company(
            name=form.cleaned_data('name'),
            symbol=form.cleaned_data('symbol'),
        )
        form = CompanyForm(request.POST, instance=company)
        if form.is_valid():
            form.save()

    context = {
        'df': df,
        'stats': stats,
        'form': form,
    }

    return render(request, 'companies/home.html', context=context)
