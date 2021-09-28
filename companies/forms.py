from django import forms
from .models import Company
from datetime import date, timedelta

TODAY = date.today()
YEAR_AGO = date.today()-timedelta(days=365)


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['symbol', 'name']


class CalculateStatsForm(forms.Form):
    date_from = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}),
                                initial=YEAR_AGO)
    date_to = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}),
                              initial=TODAY)


