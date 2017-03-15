from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import View
from .form import AssetForm, DocForm, UserForm, AssetSearchForm, DocSearchForm
from .models import Asset, Document, ApprovalAgency, AssetType, DocumentType, AssetDocument
from aetypes import template
from django.http import HttpResponse
import json, csv

class IndexView(generic.ListView):
    template_name = 'Documents/index.html'
    context_object_name = 'all_assets'
    
    def get_queryset(self):
        return Asset.objects.all()

class AssetDetailView(generic.DetailView):
    model = Asset
    template_name = 'Documents/assetDetail.html'

class UserFormView(View):
    form_class = UserForm
    template_name = 'Documents/loginPage.html'
    
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = self.form_class(None)
        username = request.POST.get('username')
        password = request.POST.get('password')  
                  
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('Documents:main')
        
        login_invalid = 'login is invalid, username or password is wrong'
        return render(request, self.template_name, {'form': form, 'error_message' :login_invalid})

@method_decorator(login_required, name='dispatch')
class AssetCreate(CreateView):
    form_class = AssetForm
    template_name = 'Documents/assetCreate.html'
    
@method_decorator(login_required, name='dispatch')
class DocCreate(CreateView):
    form_class = DocForm
    template_name = 'Documents/docCreate.html'

@method_decorator(login_required, name='dispatch')
class Search(View):
    assetform_class = AssetSearchForm
    docform_class = DocSearchForm
    template_name = 'Documents/search.html'
        
    def makeDict(self,item, search_type):
        itemDict = dict(item)
        if(search_type == "asset_search"):
            itemDict['asset_type'] = AssetType.objects.get(id=itemDict['asset_type_id']).asset_type
            itemDict['approval_agency'] = ApprovalAgency.objects.get(id=itemDict['approval_agency_id']).approval_agency 
            itemDict['search_type'] = 'asset_search'
        else:
            itemDict['asset_type'] = AssetType.objects.get(id=itemDict['asset_type_id']).asset_type
            itemDict['document_type'] = DocumentType.objects.get(id=item['document_type_id']).document_type
            itemDict['document_type_desc'] = DocumentType.objects.get(id=item['document_type_id']).document_type_desc  
            itemDict['search_type'] = 'document_search'            
        return itemDict
        
    def get(self, request):
        assetform = self.assetform_class(None)
        docform = self.docform_class(None)
        return render(request, self.template_name, {'assetform': assetform, 'docform' : docform})
     
    
    def post(self, request):  
        if(request.POST.get('search_type')):      
            if(request.POST.get('search_type') == 'asset_search'):
                result = Asset.objects.all()
                assetDict = {}
                assetDict['approval_agency_id'] = request.POST.get('approval_agency')
                assetDict['asset_type_id'] = request.POST.get('asset_type')
                assetDict['status'] = request.POST.get('status')
                assetDict['manufacture_name'] = request.POST.get('manufacture_name')
                assetDict['serial_number'] = request.POST.get('serial_number')
                assetDict['a_number'] = request.POST.get('a_number')
                assetDict['tag_number'] = request.POST.get('tag_number')
                assetDict['description'] = request.POST.get('description')
            
                for key, value in assetDict.items():
                    if key == 'asset_type_id' and value:
                        result = Asset.objects.filter(asset_type_id=value)
                    if key == 'status' and value:
                        result = Asset.objects.filter(status=value)
                    if key == 'manufacture_name' and value:
                        result = Asset.objects.filter(manufacture_name=value)
                    if key == 'approval_agency_id' and value:
                        result = Asset.objects.filter(approval_agency_id=value)
                    if key == 'serial_number' and value:
                        result = Asset.objects.filter(serial_number=value)
                    if key == 'a_number' and value:
                        document_id = Document.objects.filter(a_number=value)
                        asset_id = AssetDocument.objects.filter(id = document_id)
                        result = Asset.objects.filter(id = asset_id)
                    if key == 'tag_number' and value:
                        result = Asset.objects.filter(tag_number=value)
                    if key == 'description' and value:
                        result = Asset.objects.filter(description=value)
                
                if(result == None):
                    return HttpResponse(json.dumps("Not found"), content_type="application/json")
                
                return HttpResponse(json.dumps([self.makeDict(item, 'asset_search') for item in result.values()]), content_type="application/json")
                                            
            else:
                result = Document.objects.all()
                docDict = {}
                docDict['manufacture_name'] = request.POST.get('manufacture_name')
                docDict['document_date'] = request.POST.get('document_date')
                docDict['renewal_date'] = request.POST.get('renewal_date')
                docDict['modal_number'] = request.POST.get('modal_number')
                docDict['license_decal_number'] = request.POST.get('license_decal_number')
                docDict['a_number'] = request.POST.get('a_number')
                docDict['document_type_id'] = request.POST.get('document_type')
            
                for key, value in docDict.items():
                    if key == 'manufacture_name' and value:
                        result = Document.objects.filter(manufacture_name=value)
                    if key == 'document_date' and value:
                        result = Document.objects.filter(document_date=value)
                    if key == 'renewal_date' and value:
                        result = Document.objects.filter(renewal_date=value)
                    if key == 'modal_number' and value:
                        result = Document.objects.filter(modal_number=value)
                    if key == 'license_decal_number' and value:
                        result = Document.objects.filter(license_decal_number=value)
                    if key == 'a_number' and value:
                        result = Document.objects.filter(a_number=value)
                    if key == 'document_type_id' and value:
                        result = Document.objects.filter(document_type_id=value)
                
                if(result == None):
                    return HttpResponse(json.dumps("Not found"), content_type="application/json")
                
                return HttpResponse(json.dumps([self.makeDict(item, 'document_search') for item in result.values()]), content_type="application/json")
        
        elif(request.POST.get("export_csv")):
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="assetDetail.csv"'
            writer = csv.writer(response)
            writer.writerow(['Username', 'First name', 'Last name', 'Email address'])
            users = Asset.objects.all().values_list('username', 'first_name', 'last_name', 'email')
            for user in users:
                writer.writerow(user)

            return response
        
        else:
            return HttpResponse(json.dumps("Error"), content_type="application/json")
              
                
@login_required(login_url='Documents:login')
def main(request):       
    return render(request, 'Documents/mainPage.html')

@method_decorator(login_required, name='dispatch')
def assetEdit(request):       
    return render(request, 'Documents/assetEdit.html')

@method_decorator(login_required, name='dispatch')
def docDetail(request):       
    return render(request, 'Documents/docDetail.html')

@method_decorator(login_required, name='dispatch')
def docEdit(request):       
    return render(request, 'Documents/docEdit.html')

def logoutuser(request):
    logout(request)
    return redirect('Documents:login')

