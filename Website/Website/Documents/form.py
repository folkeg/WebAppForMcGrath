from django import forms
from .models import Asset, Document

class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ['manufacture_name', 'approval_agency', 'manufacture_serial_number', 'a_number', 'tag_number' ]

class DocForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['asset', 'manufacture_name', 'document_type', 'model_number', 'a_number', 'decal_number']
        