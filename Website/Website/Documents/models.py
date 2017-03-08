from django.db import models
from django.core.urlresolvers import reverse

class Asset(models.Model):
    manufacture_name = models.CharField(max_length=500)
    approval_agency = models.CharField(max_length=500)
    manufacture_serial_number = models.CharField(max_length=150)
    a_number = models.CharField(max_length=150)
    tag_number = models.CharField(max_length=150)
    
    def get_absolute_url(self):
        return reverse('Documents:assetCreate')
    
    def __str__(self):
        return 'a number : ' + self.a_number + ', manufacture serial number : ' + self.manufacture_serial_number

class Document(models.Model):
    asset = models.ManyToManyField(Asset)
    manufacture_name = models.CharField(max_length=500)
    document_type = models.CharField(max_length=250)
    model_number = models.CharField(max_length=150)
    a_number = models.CharField(max_length=150)
    decal_number = models.CharField(max_length=150)
    
    def get_absolute_url(self):
        return reverse('Documents:docCreate')
    
    def __str__(self):
        return 'document_type : ' + self.document_type + ', decal_number : ' + self.decal_number

