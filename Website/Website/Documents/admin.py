from django.contrib import admin
from .models import Asset, Document, AssetType, ApprovalAgency

admin.site.register(Asset)
admin.site.register(Document)
admin.site.register(AssetType)
admin.site.register(ApprovalAgency)


