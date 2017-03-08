from django import forms
from .models import Asset, Document
from django.contrib.auth.models import User

class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ['manufacture_name', 'approval_agency', 'manufacture_serial_number', 'a_number', 'tag_number' ]

class DocForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['asset', 'manufacture_name', 'document_type', 'model_number', 'a_number', 'decal_number']

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ['username', 'password']

class AssetSearchForm(forms.Form):
    manufacture_name = forms.CharField(max_length=500, required=False)
    approval_agency = forms.CharField(max_length=500, required=False)
    manufacture_serial_number = forms.CharField(max_length=150, required=False)
    a_number = forms.CharField(max_length=150, required=False)
    tag_number = forms.CharField(max_length=150, required=False)

class DocSearchForm(forms.Form):
    manufacture_name = forms.CharField(max_length=500)
    document_type = forms.CharField(max_length=250)
    model_number = forms.CharField(max_length=150)
    a_number = forms.CharField(max_length=150)
    decal_number = forms.CharField(max_length=150)

        