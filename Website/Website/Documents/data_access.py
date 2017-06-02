from .models import DocumentType, AssetType, ApprovalAgency, Asset, Document,OCRCoordinates
from django.http import HttpResponse
from datetime import date
from Finder.Files import document_file
import json, requests, csv, datetime

class SearchQuery():
    
    def searchOCRCoordinatesByDocumentType(self, document_type):
        result = OCRCoordinates.objects.filter(document_type = document_type)
        return result
    
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
            if contentDict:
                result = Asset.objects.filter(**contentDict)
            else:
                result = Asset.objects.all()
                
            if request.POST.get("manufacture_name"):            
                result = result.filter(manufacture_name__contains = request.POST.get("manufacture_name"))
            
            elif request.POST.get("serial_number"):            
                result = result.filter(serial_number__contains = request.POST.get("serial_number"))
            
            elif request.POST.get("tag_number"):            
                result = result.filter(tag_number__contains = request.POST.get("tag_number"))
            
        elif searchType == "document_search":
            if contentDict:
                result = Document.objects.filter(**contentDict)
            else:
                result = Document.objects.all()

            if request.POST.get("description"):
                result = result.filter(document_description__contains = request.POST.get("description"))
            
            elif request.POST.get("a_number"):
                result = result.filter(a_number__contains = request.POST.get("a_number"))
            
            elif request.POST.get("license_decal_number"):
                result = result.filter(license_decal_number__contains = request.POST.get("license_decal_number"))
            
            elif request.POST.get("model_number"):
                result = result.filter(model_number__contains = request.POST.get("model_number"))
            
            renewal_date_start = request.POST.get("renewal_date_start")
            renewal_date_end = request.POST.get("renewal_date_end")
            
            if renewal_date_start and renewal_date_end:
                result = result.filter(renewal_date__range = [renewal_date_start, renewal_date_end])
            
            elif renewal_date_start:
                result = result.filter(renewal_date__gte = renewal_date_start)
            
            elif renewal_date_end:
                result = result.filter(renewal_date__lte = renewal_date_start)
        
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
    
class DataExtract():
    def ocrExtract(self, filename):
        
        return None
    
class ObjectCreate():
    def documentObjectCreate(self, request):
         
        documentObject = Document(document_type_id = request.POST.get("document_type_id"),
                                 document_date = request.POST.get("document_date"), 
                                 renewal_date = request.POST.get("renewal_date") or None,
                                 a_number = request.POST.get("a_number"),
                                 license_decal_number = request.POST.get("license_decal_number"),
                                 model_number = request.POST.get("model_number"),
                                 document_description = request.POST.get("document_description"),
                                 document_file = request.FILES["document_file"])
        
        documentObject.save()
        
        if request.POST.get("asset_id"):
            assetIdArray = request.POST.get("asset_id").split(",")                  
            for assetId in assetIdArray:
                asset_id = ItemConverter().normalizeUnicodeString(assetId)
                currentAsset = Asset.objects.get(pk=asset_id)
                documentObject.asset.add(currentAsset)
            
        documentObject.save()      
        
class ObjectUpdate():
    def updateObject(self, request, documentObject):  
        
        documentObject.document_type_id = request.POST.get("document_type_id")
        documentObject.document_date = request.POST.get("document_date")
        documentObject.renewal_date = request.POST.get("renewal_date") or None
        documentObject.a_number = request.POST.get("a_number")
        documentObject.license_decal_number = request.POST.get("license_decal_number")
        documentObject.model_number = request.POST.get("model_number")
        documentObject.document_description = request.POST.get("document_description")
        
        
        if request.POST.get("document_file_content"):
            documentObject.document_file = request.FILES["document_file"]
        
        documentObject.save()
        documentObject.asset.clear()
        
        if request.POST.get("asset_id"):
            assetIdArray = request.POST.get("asset_id").split(",")
            for assetId in assetIdArray:
                asset_id = ItemConverter().normalizeUnicodeString(assetId)
                currentAsset = Asset.objects.get(pk=asset_id)
                documentObject.asset.add(currentAsset)
        
        documentObject.save()

class UserActivityLog():
    def logUserActivity(self, username, event):
        logDict = {}
        logDict['Time'] = datetime.datetime.now()
        logDict['User'] = username
        logDict['Event'] = event
        with open('userActivityLog.csv', 'a') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(logDict.values())
             
        
        
        