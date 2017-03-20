from django import forms
from .models import Asset, Document, AssetType, ApprovalAgency, DocumentType, StatusChoices
from django.contrib.auth.models import User

class AssetCreateForm(forms.ModelForm): 
    
    approval_agency = forms.ModelChoiceField(queryset = ApprovalAgency.objects.all())
    asset_type = forms.ModelChoiceField(queryset = AssetType.objects.all())
    
    class Meta:
        model = Asset
        fields = ['approval_agency', 'asset_type', 'manufacture_name', 'serial_number', 'tag_number', 'status']   
        
class DocCreateForm(forms.ModelForm):
    
    document_type = forms.CharField(max_length=500)
    
    class Meta:
        model = Document
        fields = ['document_type', 'document_date', 'renewal_date', 'a_number', 'license_decal_number', 'model_number', 'document_description']
        
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ['username', 'password']

class AssetSearchForm(forms.Form):
    approval_agency = forms.ModelChoiceField(queryset = ApprovalAgency.objects.all(), required=False)
    asset_type = forms.ModelChoiceField(queryset = AssetType.objects.all(), required=False)
    manufacture_name = forms.CharField(required=False)
    serial_number = forms.CharField(required=False)
    tag_number = forms.CharField(required=False)
    status = forms.ChoiceField(choices = StatusChoices, required=False)

class DocSearchForm(forms.Form):
    document_type = forms.CharField(required=False)
    document_date = forms.DateField(required=False)
    renewal_date = forms.DateField(required=False)
    manufacture_name = forms.CharField(required=False)
    a_number = forms.CharField(required=False)
    license_decal_number = forms.CharField(required=False)
    model_number = forms.CharField(required=False)
    description = forms.CharField(required=False)

class AssetLinkForm(forms.Form):
    serial_number = forms.CharField(required=False)
    tag_number = forms.CharField(required=False)

        