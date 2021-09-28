from django import forms


class CalculatePortfoliosForm(forms.Form):
    rf = forms.FloatField(initial=1)