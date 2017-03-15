from django.db import models
from django.core.urlresolvers import reverse
from .utils import StatusChoices 
from datetime import datetime

class AssetType(models.Model):
    asset_type = models.CharField(max_length = 500)
    
    def __str__(self):
        return self.asset_type

class ApprovalAgency(models.Model):
    approval_agency = models.CharField(max_length = 500)
    
    def __str__(self):
        return self.approval_agency

class AssetDocument(models.Model):
    asset = models.ForeignKey('Asset')
    document = models.ForeignKey('Document')
    
    def __str__(self):
        return self.asset + self.document

class DocumentType(models.Model):
    asset_type = models.ForeignKey(AssetType)
    document_type = models.CharField(max_length = 500)
    document_type_desc = models.CharField(max_length = 500, blank = True)
    
    def __str__(self):
        return self.document_type
        
class Asset(models.Model):
    approval_agency = models.ForeignKey(ApprovalAgency)
    asset_type = models.ForeignKey(AssetType)
    manufacture_name = models.CharField(max_length = 500, blank = True)
    serial_number = models.CharField(max_length = 500, blank = True)
    status = models.CharField(max_length = 500, choices = StatusChoices, blank =True)
    tag_number = models.CharField(max_length = 500, blank = True)
    description = models.CharField(max_length = 500, blank = True)
    
    
    def get_absolute_url(self):
        return reverse('Documents:assetCreate')
    
    def __str__(self):
        return self.manufacture_name + ',' +self.serial_number + ',' +self.tag_number + ',' +self.status + ',' +self.description

class Document(models.Model):
    asset_type = models.ForeignKey(AssetType)
    document_type = models.ForeignKey(DocumentType)
    document_date = models.DateField(default = datetime.now)
    renewal_date = models.DateField(blank = True, null=True)
    manufacture_name = models.CharField(max_length = 500, blank = True)
    model_number = models.CharField(max_length = 500, blank = True)
    a_number = models.CharField(max_length = 500, blank = True)
    license_decal_number = models.CharField(max_length = 500, blank = True)
    document_description = models.CharField(max_length = 500, blank = True)
    
    def get_absolute_url(self):
        return reverse('Documents:docCreate')
    
    def __str__(self):
        return self.model_number + ',' + self.manufacture_name + ',' + self.a_number + ',' + self.license_decal_number + ',' + self.document_description



