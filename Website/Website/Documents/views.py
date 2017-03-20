from django.views import generic
from django.views.generic.edit import CreateView, UpdateView
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import View
from .form import AssetCreateForm, DocCreateForm, UserForm, AssetSearchForm, DocSearchForm, AssetLinkForm
from .models import Asset, Document, ApprovalAgency, AssetType, DocumentType
from aetypes import template
from django.http import HttpResponse
import json, csv
from .utils import SearchQuery, CSVCreate, ObjectCreate

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
    
    form_class = AssetCreateForm
    template_name = 'Documents/assetCreate.html'
       
@method_decorator(login_required, name='dispatch')
class DocCreate(View):
    
    docform_class = DocCreateForm
    template_name = 'Documents/docCreate.html'
    
    def get(self, request):
        
        docform = self.docform_class(None)
        
        return render(request, self.template_name, {'docform' : docform})
    
    def post(self, request):
        
        docform = self.docform_class(None)
        
        if(request.POST.get("asset_id")): 
            
            ObjectCreate().documentObjectCreate(request)    
                               
            return render(request, self.template_name, {'docform': docform})
        
        elif(request.POST.get("document_type")):

            return SearchQuery().searchByDocumentType(request)
            
        elif(self.request.POST.get("search_type")):

            attributeList = ['serial_number', 'tag_number']
            
            return SearchQuery().searchContent(request, attributeList, 'asset_search')
     

@method_decorator(login_required, name='dispatch')
class Search(View):
    
    assetform_class = AssetSearchForm
    docform_class = DocSearchForm
    template_name = 'Documents/search.html'
        
    def get(self, request):
        
        assetform = self.assetform_class(None)
        docform = self.docform_class(None)
        
        return render(request, self.template_name, {'assetform': assetform, 'docform' : docform})
         
    def post(self, request):  
        
        if(request.POST.get('search_type')):      
            if(request.POST.get('search_type') == 'asset_search'):
                
                attributeList = ['approval_agency', 'asset_type', 'manufacture_name', 'serial_number', 'tag_number', 'status']
                
                return SearchQuery().searchContent(request, attributeList, 'asset_search')
            else:
                
                attributeList = ['document_type', 'document_date', 'renewal_date', 'a_number', 'license_decal_number', 'model_number', 'description']
                
                return SearchQuery().searchContent(request, attributeList, 'document_search')
        #to be revised
        elif(request.POST.get("export_csv")):
            
            return CSVCreate().csvCreate(request)
        
        elif(request.POST.get("document_type")):
            
            return SearchQuery().searchByDocumentType(request)
        
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

