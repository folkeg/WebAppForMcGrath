from .models import DocumentType, AssetType, ApprovalAgency, Asset, Document
from django.http import HttpResponse
import json, csv

class SearchQuery():
    def searchByDocumentType(self, request):
        document_type_request = request.POST.get("document_type")
        result = DocumentType.objects.filter(document_type__istartswith=document_type_request)
        return HttpResponse(json.dumps([ItemConverter().convertToDict(item, 'document_type') for item in result.values()]), content_type="application/json")
       
    def searchContent(self, request, attributeList, searchType):
        contentDict = {}
        
        for field in attributeList:
            if request.POST.get(field):
                contentDict[field] = request.POST.get(field)
                
        result = Asset.objects.filter(**contentDict)
        
        if not result.exists():
            return HttpResponse(json.dumps("Not found"), content_type="application/json")
        
        return HttpResponse(json.dumps([ItemConverter().convertToDict(item, searchType) for item in result.values()]), content_type="application/json")                                           
    
class CSVCreate():
    def csvCreate(self, request):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="assetDetail.csv"'
        writer = csv.writer(response)
        writer.writerow(['Username', 'First name', 'Last name', 'Email address'])
        users = Asset.objects.all().values_list('username', 'first_name', 'last_name', 'email')
        for user in users:
            writer.writerow(user)

        return response

class ItemConverter():
    def convertToDict(self, item, search_type):
        itemDict = dict(item)
        if(search_type == "asset_search"):
            itemDict['asset_type'] = AssetType.objects.get(id=itemDict['asset_type_id']).asset_type
            itemDict['approval_agency'] = ApprovalAgency.objects.get(id=itemDict['approval_agency_id']).approval_agency 
        elif(search_type == "document_search"):

            itemDict['document_type'] = DocumentType.objects.get(id=item['document_type_id']).document_type
            itemDict['document_type_desc'] = DocumentType.objects.get(id=item['document_type_id']).document_type_desc        
        return itemDict