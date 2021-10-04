from django import forms
from .models import BoughtPortfolio


class CalculatePortfoliosForm(forms.Form):
    rf = forms.FloatField(initial=1)


class BoughtPortfolioForm(forms.ModelForm):
    class Meta:
        model = BoughtPortfolio
        fields = ['budget']
