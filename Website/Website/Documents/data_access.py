from .models import DocumentType, AssetType, ApprovalAgency, Asset, Document
from django.http import HttpResponse
from datetime import date
import json
from CodeWarrior.Standard_Suite import document

class SearchQuery():
    
    def searchDocumentTypeByAutoComplete(self, document_type_prefix):        
        result = DocumentType.objects.filter(document_type__istartswith=document_type_prefix)
        return HttpResponse(json.dumps([ItemConverter().convertToDict(item, 'not_necessary') for item in result.values()]), content_type="application/json")
    
    def searchDocumentsByAssetId(self, asset_id):        
        asset_data = Asset.objects.filter(pk = asset_id)
        result = Document.objects.filter(asset = asset_data)
        return HttpResponse(json.dumps([ItemConverter().convertToDict(item, 'document_search') for item in result.values()]), content_type="application/json")
    
    def searchLinkedAssetsByDocumentId(self, document_object):            
        result = document_object.asset.all()
        return json.dumps([ItemConverter().convertToDict(item, 'asset_search') for item in result.values()])
        
    def searchAssetTypesByApprovalAgency(self, approval_agency_id):
        approval_agency = ApprovalAgency.objects.filter(pk = approval_agency_id)
        result = AssetType.objects.filter(approval_agency = approval_agency)
        return HttpResponse(json.dumps([ItemConverter().convertToDict(item, 'not_necessary') for item in result.values('id', 'asset_type')]), content_type="application/json")      
        
    def searchAssetOrDocumentObjects(self, request, attributeList, searchType):
        contentDict = {}       
        for field in attributeList:
            if request.POST.get(field):
                contentDict[field] = request.POST.get(field)
        
        if searchType == "asset_search":
            result = Asset.objects.filter(**contentDict)
            
        elif searchType == "document_search":
            result = Document.objects.filter(**contentDict)
        
        if not result.exists():
            return HttpResponse(json.dumps("Not found"), content_type="application/json")
            
        return HttpResponse(json.dumps([ItemConverter().convertToDict(item, searchType) for item in result.values()]), content_type="application/json")                                           

class ItemConverter():
    def convertToJsonSerial(self, obj, itemDict):
        item = itemDict[obj]
        if isinstance(item, date):
            serial = item.isoformat()
            itemDict[obj] = serial
    
    def convertToDict(self, item, search_type):
        itemDict = dict(item)
        if search_type == "asset_search":
            itemDict['asset_type'] = AssetType.objects.get(id=itemDict['asset_type_id']).asset_type
            itemDict['approval_agency'] = ApprovalAgency.objects.get(id=itemDict['approval_agency_id']).approval_agency 
            
        elif search_type == "document_search":          
            self.convertToJsonSerial('document_date', itemDict)
            self.convertToJsonSerial('renewal_date', itemDict)      
            itemDict['document_type'] = DocumentType.objects.get(id=item['document_type_id']).document_type
            itemDict['document_type_desc'] = DocumentType.objects.get(id=item['document_type_id']).document_type_desc    
             
        return itemDict
    
    def normalizeUnicodeString(self, x):
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
            asset_id = ItemConverter().normalizeUnicodeString(assetId)
            currentAsset = Asset.objects.get(pk=asset_id)
            documentObject.asset.add(currentAsset)
        
        documentObject.save()           
        
class UpdateObject():
    def updateLinkedAssetsByDocument(self, request, documentObject):  
        
        assetIdArray = request.POST.get("asset_id").split(",")
        documentObject.asset.clear()
        for assetId in assetIdArray:
            asset_id = ItemConverter().normalizeUnicodeString(assetId)
            currentAsset = Asset.objects.get(pk=asset_id)
            documentObject.asset.add(currentAsset)
        
        documentObject.save()
             
        
        
        