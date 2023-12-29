from django import forms

class CompanyForm(forms.Form):
    ticker=forms.CharField()

