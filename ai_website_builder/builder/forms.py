from django import forms

class WebsiteForm(forms.Form):
    name = forms.CharField(label="Business Name", max_length=100)
    business_type = forms.CharField(label="Business Type", max_length=100)
    industry = forms.CharField(label="Industry", max_length=100)
