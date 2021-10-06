from django import forms

from .models import Company


class ImageCompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['image']
