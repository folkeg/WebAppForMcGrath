from django.views import generic
from django.views.generic.edit import CreateView, UpdateView
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import View
from .form import AssetCreateForm, DocCreateForm, UserForm, AssetSearchForm, DocSearchForm, AssetLinkForm, DocEditForm
from .models import Asset, Document, ApprovalAgency, AssetType, DocumentType
from aetypes import template
from django.http import HttpResponse, Http404
import json
from .data_access import SearchQuery, ObjectCreate, UpdateObject
from django.core.urlresolvers import reverse_lazy
from django.views.generic.detail import DetailView



@method_decorator(login_required, name='dispatch')
class AssetEditView(UpdateView):

    model = Asset
    fields = ['approval_agency', 'asset_type', 'manufacture_name', 'serial_number', 'tag_number', 'status']
    template_name = 'Documents/assetEdit.html'
    
    def get_success_url(self):
        return reverse_lazy('Documents:search')


@method_decorator(login_required, name='dispatch')
class DocumentEditView(UpdateView):

    model= Document
    form_class = DocEditForm
    second_form_class = AssetLinkForm
    template_name = 'Documents/documentEdit.html'

    def get_context_data(self, **kwargs):
        asset_objects = SearchQuery().searchLinkedAssetsByDocumentId(self.object)
        context = super(DocumentEditView, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class(self.request.GET)
        if 'asset_link_form' not in context:
            context['asset_link_form'] = self.second_form_class(self.request.GET)
        context['asset_objects'] = asset_objects
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        
        if request.POST.get('search_type'):
            attributeList = ['approval_agency', 'serial_number', 'tag_number']            
            return SearchQuery().searchAssetOrDocumentObjects(request, attributeList, 'asset_search')
        
        elif request.POST.get('document_date'):
            UpdateObject().updateLinkedAssetsByDocument(request, self.object)
                                
        return super(UpdateView, self).post(request, *args, **kwargs)
    
    def get_success_url(self):
        return reverse_lazy('Documents:search')


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
    
    def get(self, request, *args, **kwargs):       
        if request.GET.get('approval_agency'):                        
            return SearchQuery().searchAssetTypesByApprovalAgency(request.GET.get('approval_agency'))        
        self.object = None
        return super(CreateView, self).get(request, *args, **kwargs)
 
       
@method_decorator(login_required, name='dispatch')
class DocCreate(View):
    
    docform_class = DocCreateForm
    asset_link_form_class = AssetLinkForm
    template_name = 'Documents/docCreate.html'
    
    def get(self, request):        
        docform = self.docform_class(None)
        asset_link_form = self.asset_link_form_class(None)       
        return render(request, self.template_name, {'docform' : docform, 'asset_link_form' : asset_link_form})
    
    def post(self, request):       
        if request.POST.get("document_date"):    
            ObjectCreate().documentObjectCreate(request)                              
            return self.get(request)
        
        elif request.POST.get("document_type"):
            return SearchQuery().searchDocumentTypeByAutoComplete(request.POST.get("document_type"))
            
        elif self.request.POST.get("search_type"):
            attributeList = ['approval_agency', 'serial_number', 'tag_number']            
            return SearchQuery().searchAssetOrDocumentObjects(request, attributeList, 'asset_search')
     

@method_decorator(login_required, name='dispatch')
class Search(View):
    
    assetform_class = AssetSearchForm
    docform_class = DocSearchForm
    template_name = 'Documents/search.html'
        
    def get(self, request):
        if request.GET.get('approval_agency'):                        
            return SearchQuery().searchAssetTypesByApprovalAgency(request.GET.get('approval_agency'))
                                    
        elif request.GET.get('asset_id'):            
            return SearchQuery().searchDocumentsByAssetId(request.GET.get('asset_id'))
            
        else:          
            assetform = self.assetform_class(None)
            docform = self.docform_class(None)
            
            return render(request, self.template_name, {'assetform': assetform, 'docform' : docform})         
            
         
    def post(self, request):  
        if request.POST.get('search_type'):      
            if(request.POST.get('search_type') == 'asset_search'):              
                attributeList = ['approval_agency', 'asset_type', 'manufacture_name', 'serial_number', 'tag_number', 'status']                
                return SearchQuery().searchAssetOrDocumentObjects(request, attributeList, 'asset_search')
            
            else:                
                attributeList = ['document_type_id', 'document_date', 'renewal_date', 'a_number', 'license_decal_number', 'model_number', 'description']                
                return SearchQuery().searchAssetOrDocumentObjects(request, attributeList, 'document_search')
        
        elif request.POST.get("document_type"):            
            return SearchQuery().searchDocumentTypeByAutoComplete(request.POST.get("document_type"))
        
        else:            
            return HttpResponse(json.dumps("Error"), content_type="application/json")
              
@method_decorator(login_required, name='dispatch')
class DocDetail(DetailView):
    
    model = Document
    template_name = 'Documents/docDetail.html'
       
    def get(self, request, pk):
        
        return render(request, self.template_name, {'docFile' : self.get_object().document_file})
    
               
@login_required(login_url='Documents:login')
def main(request):      
     
    return render(request, 'Documents/mainPage.html')
    
def logoutuser(request):
    
    logout(request)
    
    return redirect('Documents:login')

