from django.db import models
from django.core.urlresolvers import reverse
from datetime import datetime

StatusChoices = (
    (None, "-----"),
    ("Active", "Active"),
    ("Sold", "Sold")
)

class ApprovalAgency(models.Model):
    approval_agency = models.CharField(max_length = 500)
    
    def __str__(self):
        return self.approval_agency


class AssetType(models.Model):
    approval_agency = models.ForeignKey(ApprovalAgency)
    asset_type = models.CharField(max_length = 500)
    
    def __str__(self):
        return self.asset_type

class DocumentType(models.Model):
    document_type = models.CharField(max_length = 500)
    document_type_desc = models.CharField(max_length = 500, blank = True)
    
    def __str__(self):
        return self.document_type + " " + self.document_type_desc
        
class Asset(models.Model):
    approval_agency = models.ForeignKey(ApprovalAgency)
    asset_type = models.ForeignKey(AssetType)
    manufacture_name = models.CharField(max_length = 500, blank = True)
    serial_number = models.CharField(max_length = 500)
    tag_number = models.CharField(max_length = 500, blank = True)
    status = models.CharField(max_length = 500, choices = StatusChoices, blank =True)
    
    def get_absolute_url(self):
        return reverse('Documents:assetCreate')
    
    def __str__(self):
        return str("serial number: " + self.serial_number + " , tag number: " + self.tag_number)

class Document(models.Model):
    asset = models.ManyToManyField(Asset, blank=True)
    document_type = models.ForeignKey(DocumentType)
    document_date = models.DateField()
    renewal_date = models.DateField(blank = True, null=True)
    a_number = models.CharField(max_length = 500, blank = True)
    license_decal_number = models.CharField(max_length = 500, blank = True)
    model_number = models.CharField(max_length = 500, blank = True)
    document_description = models.CharField(max_length = 500, blank = True)
    document_file = models.FileField(upload_to='uploads/%Y/%m/%d/')
    
    def get_absolute_url(self):
        return reverse('Documents:docCreate')
    
    def __str__(self):
        return  str(self.id) + " " + str(self.document_date) + " " + str(self.renewal_date) + " " + str(self.a_number) + " " + str(self.license_decal_number) + " " + str(self.model_number) + " " +str(self.document_description)

class OCRCoordinates(models.Model):
    document_type = models.ForeignKey(DocumentType)
    document_date_left = models.CharField(max_length = 500)
    
    document_date_top = models.CharField(max_length = 500)
    document_date_right = models.CharField(max_length = 500)
    
    document_date_bottom = models.CharField(max_length = 500)
    document_date_letterset = models.CharField(max_length = 500, blank = True)
    document_date_Regex = models.CharField(max_length = 500, blank = True)
    
    document_date_MarkingType = models.CharField(max_length = 500, blank = True)
    locument_date_texttype = models.CharField(max_length = 500, blank = True)
    
    license_decal_left = models.CharField(max_length = 500)
    license_decal_top = models.CharField(max_length = 500)
    license_decal_right = models.CharField(max_length = 500)
    license_decal_bottom = models.CharField(max_length = 500)
    license_decal_letterset = models.CharField(max_length = 500, blank = True)
    license_decal_Regex = models.CharField(max_length = 500, blank = True)
    license_decal_Markingtype = models.CharField(max_length = 500, blank = True)
    license_decal_texttype = models.CharField(max_length = 500, blank = True)
    
    renewal_date_left = models.CharField(max_length = 500)
    renewal_date_top = models.CharField(max_length = 500)
    renewal_date_right = models.CharField(max_length = 500)
    renewal_date_bottom = models.CharField(max_length = 500)
    renewal_date_letterset = models.CharField(max_length = 500, blank = True)
    renewal_date_regex = models.CharField(max_length = 500, blank = True)
    renewal_date_texttype = models.CharField(max_length = 500, blank = True)
    
    def __str__(self):
        return str(self.id) + " " + str(self.document_type) + " " + str(self.document_date_top)

