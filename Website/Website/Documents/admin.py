from django.contrib import admin
from .models import Asset, Document, AssetType, ApprovalAgency, DocumentType

admin.site.register(Asset)
admin.site.register(Document)
admin.site.register(AssetType)
admin.site.register(ApprovalAgency)
admin.site.register(DocumentType)


