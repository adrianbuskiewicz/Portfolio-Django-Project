from django.shortcuts import render, redirect, reverse, get_object_or_404
from .models import Company, FinancialProfile
from .utils_financial import company_df, df_mean_price, df_vol_price, corr_matrix
from .forms import CompanyForm, CalculateStatsForm

# Create your views here.


def home_view(request):
    companies = Company.objects.filter(user=request.user).order_by(
        '-financialprofile__rate_of_return',
        'financialprofile__volatility',
    )
    if request.method == 'POST':
        create_company_form = CompanyForm(request.POST)
        calculate_stats_form = CalculateStatsForm(request.POST)
        if create_company_form.is_valid():
            company = create_company_form.save(commit=False)
            company.user = request.user
            company.save()
            financialprofile = FinancialProfile(company=company)
            financialprofile.save()
        if calculate_stats_form.is_valid():
            symbols = []
            date_from = calculate_stats_form.cleaned_data.get('date_from')
            date_to = calculate_stats_form.cleaned_data.get('date_to')
            for company in companies:
                symbols.append(company.symbol)
                r_o_r = df_mean_price(
                    symbol=company.symbol,
                    date_from=date_from,
                    date_to=date_to
                )
                vol = df_vol_price(
                    symbol=company.symbol,
                    date_from=date_from,
                    date_to=date_to,
                )
                FinancialProfile.objects.filter(company=company).update(
                    rate_of_return=r_o_r,
                    volatility=vol,
                    start_date=date_from,
                    end_date=date_to,

                )
            df = company_df(symbols, date_from=date_from, date_to=date_to)
            df_style = 'class="table table-striped table-dark table-hover"'
            corr_mat = corr_matrix(df, style=df_style)
            request.session['date_from'] = date_from.strftime("%d.%m.%Y")
            request.session['date_to'] = date_to.strftime("%d.%m.%Y")
            request.session['corr_mat'] = corr_mat
        return redirect(reverse('companies:home'))
    else:
        create_company_form = CompanyForm()
        calculate_stats_form = CalculateStatsForm()
        edit_company_form = CompanyForm()

    context = {
        'companies': companies,
        'create_company_form': create_company_form,
        'calculate_stats_form': calculate_stats_form,
        'edit_company_form': edit_company_form,
    }

    return render(request, 'companies/home.html', context=context)


def delete_company_view(request, pk):
    company_to_delete = get_object_or_404(Company, pk=pk)
    if request.method == 'POST':
        company_to_delete.delete()
        return redirect(reverse('companies:home'))


def edit_company_view(request, pk):
    company_to_edit = get_object_or_404(Company, pk=pk)
    if request.method == 'POST':
        edit_company_form = CompanyForm(request.POST or None,
                                        instance=company_to_edit)
        if edit_company_form.is_valid():
            edit_company_form.save()
            return redirect(reverse('companies:home'))


def use_company_view(request, pk):
    company_to_use = get_object_or_404(Company, pk=pk)
    if request.method == 'POST':
        if company_to_use.used_in_portfolio == 'yes':
            company_to_use.used_in_portfolio = 'no'
        else:
            company_to_use.used_in_portfolio = 'yes'
        company_to_use.save()
        return redirect(reverse('companies:home'))


