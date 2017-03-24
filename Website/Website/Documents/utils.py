from .models import DocumentType, AssetType, ApprovalAgency, Asset, Document
from django.http import HttpResponse
from datetime import date
import json, csv

class SearchQuery():
    def searchByDocumentType(self, request):
        document_type_request = request.POST.get("document_type")
        result = DocumentType.objects.filter(document_type__istartswith=document_type_request)
        return HttpResponse(json.dumps([ItemConverter().convertToDict(item, 'document_type') for item in result.values()]), content_type="application/json")
    
    def searchByAssetId(self, request):
        asset_id = request.GET.get("asset_id")
        asset_data = Asset.objects.filter(pk = asset_id)
        result = Document.objects.filter(asset = asset_data)
        return HttpResponse(json.dumps([ItemConverter().convertToDict(item, 'document_search') for item in result.values()]), content_type="application/json")
       
    def searchContent(self, request, attributeList, searchType):
        contentDict = {}
        
        for field in attributeList:
            if request.POST.get(field):
                contentDict[field] = request.POST.get(field)
        
        if(searchType == "asset_search"):
            result = Asset.objects.filter(**contentDict)
            
        elif(searchType == "document_search"):
            result = Document.objects.filter(**contentDict)
        
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
    def convertToJsonSerial(self, obj, itemDict):
        item = itemDict[obj]
        if isinstance(item, date):
            serial = item.isoformat()
            itemDict[obj] = serial
    
    def convertToDict(self, item, search_type):
        print search_type
        itemDict = dict(item)
        if(search_type == "asset_search"):
            itemDict['asset_type'] = AssetType.objects.get(id=itemDict['asset_type_id']).asset_type
            itemDict['approval_agency'] = ApprovalAgency.objects.get(id=itemDict['approval_agency_id']).approval_agency 
        elif(search_type == "document_search"):
            self.convertToJsonSerial('document_date', itemDict)
            self.convertToJsonSerial('renewal_date', itemDict)
       
            itemDict['document_type'] = DocumentType.objects.get(id=item['document_type_id']).document_type
            itemDict['document_type_desc'] = DocumentType.objects.get(id=item['document_type_id']).document_type_desc      
        return itemDict
    
    def byte_string(self, x):
        return str(x) if isinstance(x, unicode) else x

class ObjectCreate():
    def documentObjectCreate(self, request):
        documentObject = Document(document_type_id = request.POST.get("document_type_id"),
                                     document_date = request.POST.get("document_date"), 
                                     renewal_date = request.POST.get("renewal_date") or None,
                                     a_number = request.POST.get("a_number"),
                                     license_decal_number = request.POST.get("license_decal_number"),
                                     model_number = request.POST.get("model_number"),
                                     document_description = request.POST.get("document_description"))

        documentObject.save()
        
        assetIdArray = request.POST.get("asset_id").split(",")
                    
        for assetId in assetIdArray:
            asset_id = ItemConverter().byte_string(assetId)
            currentAsset = Asset.objects.get(pk=asset_id)
            documentObject.asset.add(currentAsset)
        
        documentObject.save()           
        
        
        
        
        