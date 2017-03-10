from django.db import models
from django.core.urlresolvers import reverse
from .utils import ApprovalAgencyChoices, AssetTypeChoices, StatusChoices, DocumentTypeChoices

class Asset(models.Model):
    manufacture_name = models.CharField(max_length = 500)
    approval_agency = models.CharField(max_length = 500, choices = ApprovalAgencyChoices)
    asset_type = models.CharField(max_length = 500, choices = AssetTypeChoices)
    serial_number = models.CharField(max_length = 500)
    a_number = models.CharField(max_length = 500)
    tag_number = models.CharField(max_length = 500)
    status = models.CharField(max_length = 500, choices = StatusChoices)
    description = models.CharField(max_length = 500, null=True)
    
    def get_absolute_url(self):
        return reverse('Documents:assetCreate')
    
    def __str__(self):
        return self.approval_agency + ',' + self.asset_type + ',' +self.manufacture_name + ',' +self.a_number + ',' +self.serial_number + ',' +self.tag_number + ',' +self.status + ',' +self.description

class Document(models.Model):
    asset = models.ManyToManyField(Asset)
    manufacture_name = models.CharField(max_length = 500)
    document_type = models.CharField(max_length = 500, choices = DocumentTypeChoices)
    document_date = models.CharField(max_length = 500, null=True)
    renewal_date = models.CharField(max_length = 500, null=True)
    model_number = models.CharField(max_length = 500, null=True)
    a_number = models.CharField(max_length = 500, null=True)
    license_decal_number = models.CharField(max_length = 500, null=True)
    document_description = models.CharField(max_length = 500, null=True)
    
    def get_absolute_url(self):
        return reverse('Documents:docCreate')
    
    def __str__(self):
        return self.document_type + ',' + self.document_date + ',' + self.renewal_date + ',' + self.model_number + ',' + self.manufacture_name + ',' + self.a_number + ',' + self.license_decal_number + ',' + self.document_description

