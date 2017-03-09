from django import forms
from .models import Asset, Document
from django.contrib.auth.models import User

class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ['approval_agency', 'asset_type', 'manufacture_name', 'serial_number', 'a_number', 'tag_number', 'status', 'description']
class DocForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['asset', 'document_type', 'document_date', 'renewal_date', 'manufacture_name', 'model_number', 'a_number', 'license_decal_number', 'document_description']
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ['username', 'password']

class AssetSearchForm(forms.Form):
    approval_agency = forms.CharField(required=False)
    asset_type = forms.CharField(required=False)
    manufacture_name = forms.CharField(required=False)
    serial_number = forms.CharField(required=False)
    status = forms.CharField(required=False)
    a_number = forms.CharField(required=False)
    tag_number = forms.CharField(required=False)

class DocSearchForm(forms.Form):
    document_type = forms.CharField(required=False)
    manufacture_name = forms.CharField(required=False)
    document_date = forms.CharField(required=False)
    renewal_date = forms.CharField(required=False)
    model_number = forms.CharField(required=False)
    a_number = forms.CharField(required=False)
    license_decal_number = forms.CharField(required=False)

        