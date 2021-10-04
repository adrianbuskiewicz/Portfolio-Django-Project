from django.shortcuts import render, redirect, reverse, get_object_or_404
from .models import Company, FinancialProfile
from .utils_financial import company_df, df_mean_price, df_vol_price, corr_matrix
from .forms import CompanyForm, CalculateStatsForm
from django.contrib import messages

# Create your views here.


def home_view(request):
    # Companies created by our user
    companies = Company.objects.filter(user=request.user).order_by(
        '-financialprofile__rate_of_return',
        'financialprofile__volatility',
    )
    if request.method == 'POST':
        create_company_form = CompanyForm(request.POST)
        calculate_stats_form = CalculateStatsForm(request.POST)
        if create_company_form.is_valid():
            # Checking if our user already got company named like this
            existing_company = companies.filter(symbol=create_company_form.cleaned_data.get('symbol')).first()
            if existing_company:
                messages.error(request, "Company already exists!")
            else:
                # Saving company with our user's id
                company = create_company_form.save(commit=False)
                company.user = request.user
                company.save()
                financialprofile = FinancialProfile(company=company)
                financialprofile.save()
                messages.success(request, "Company added!")
        if calculate_stats_form.is_valid():
            # We calculate our companies stats (rates and volatility) and create correlation matrix
            symbols = []
            date_from = calculate_stats_form.cleaned_data.get('date_from')
            date_to = calculate_stats_form.cleaned_data.get('date_to')
            for company in companies:
                # We use already existing loop to catch our symbols
                symbols.append(company.symbol)
                # Calculating rates and volatility for every company
                r_o_r = df_mean_price(
                    symbol=company.symbol,
                    date_from=date_from,
                    date_to=date_to,
                )
                vol = df_vol_price(
                    symbol=company.symbol,
                    date_from=date_from,
                    date_to=date_to,
                )
                # Updating company' profile with every calc
                FinancialProfile.objects.filter(company=company).update(
                    rate_of_return=r_o_r,
                    volatility=vol,
                    start_date=date_from,
                    end_date=date_to,
                )
            # Correlation matrix styles as table
            df = company_df(symbols, date_from=date_from, date_to=date_to)
            df_style = 'class="table table-striped table-dark table-hover"'
            corr_mat = corr_matrix(df, style=df_style)
            # Put it in session to do not need to create all the time new matrix
            request.session['corr_mat'] = corr_mat
            messages.success(request, "Companies stats calculated!")
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
        'start_date': companies[0].financialprofile.start_date if companies else None,
        'end_date': companies[0].financialprofile.end_date if companies else None,
    }

    return render(request, 'companies/home.html', context=context)


def delete_company_view(request, pk):
    # Deleting unwanted anymore companies in our user's db
    company_to_delete = get_object_or_404(Company, pk=pk)
    if company_to_delete.user == request.user:
        company_to_delete.delete()
        messages.info(request, 'Company deleted!')
        return redirect(reverse('companies:home'))
    else:
        messages.error(request, "You cannot delete this company, because u ain't right user!")
        return redirect(reverse('companies:home'))


def edit_company_view(request, pk):
    # Editing company symbol or name
    company_to_edit = get_object_or_404(Company, pk=pk)
    if request.method == 'POST':
        edit_company_form = CompanyForm(request.POST or None,
                                        instance=company_to_edit)
        if edit_company_form.is_valid():
            edit_company_form.save()
            messages.info(request, 'Company updated!')
            return redirect(reverse('companies:home'))


def use_company_view(request, pk):
    # Changing status of companies (to be used in portfolio or not)
    company_to_use = get_object_or_404(Company, pk=pk)
    if request.method == 'POST':
        if company_to_use.used_in_portfolio == 'yes':
            company_to_use.used_in_portfolio = 'no'
        else:
            company_to_use.used_in_portfolio = 'yes'
        company_to_use.save()
        return redirect(reverse('companies:home')+'#use_companies_table')


