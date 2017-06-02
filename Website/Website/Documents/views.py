import os
from django.views.generic.edit import CreateView, UpdateView
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import View
from .form import AssetCreateForm, DocCreateForm, UserForm, AssetSearchForm, DocSearchForm, AssetLinkForm, DocEditForm
from .models import Asset, Document
from django.http import HttpResponse
import json, datetime
from .data_access import SearchQuery, ObjectCreate, ObjectUpdate, DataExtract, UserActivityLog
from django.core.urlresolvers import reverse_lazy
from django.views.generic.detail import DetailView
import ocrizer

@method_decorator(login_required, name='dispatch')
class AssetEditView(UpdateView):

    model = Asset
    fields = ['approval_agency', 'asset_type', 'manufacture_name', 'serial_number', 'tag_number', 'status']
    template_name = 'Documents/assetEdit.html'
    
    def get_success_url(self):
        UserActivityLog().logUserActivity(self.request.user.username, "Asset Changed")  
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
        
        context['asset_link_form'] = self.second_form_class(self.request.GET)        
        context['document_type_object'] = self.object.document_type
        context['asset_objects'] = asset_objects
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        
        if request.POST.get('search_type'):
            attributeList = ['approval_agency', 'serial_number', 'tag_number']            
            return SearchQuery().searchAssetOrDocumentObjects(request, attributeList, 'asset_search')
        
        elif request.POST.get('document_date'):
            ObjectUpdate().updateObject(request, self.object)
            UserActivityLog().logUserActivity(self.request.user.username, "Document Changed") 
            return redirect('Documents:search')
        
        elif request.POST.get("document_type"):
            return SearchQuery().searchDocumentTypeByAutoComplete(request.POST.get("document_type"))
                                
    def get_success_url(self):
        UserActivityLog().logUserActivity(self.request.user.username, "Document Changed") 
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
                UserActivityLog().logUserActivity(username, 'login')           
                login(request, user)                
                return redirect('Documents:main')   
        else:    
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
    
    def post(self, request, *args, **kwargs):
        
        UserActivityLog().logUserActivity(request.user.username, "Asset Create Completed")   
        
        return CreateView.post(self, request, *args, **kwargs)
 
       
@method_decorator(login_required, name='dispatch')
class DocCreate(View):
    coordinate_result = ""
    document_file_name = ""
    
    docform_class = DocCreateForm
    asset_link_form_class = AssetLinkForm
    template_name = 'Documents/docCreate.html'
    
    def get(self, request):        
        docform = self.docform_class(None)
        asset_link_form = self.asset_link_form_class(None)       
        return render(request, self.template_name, {'docform' : docform, 'asset_link_form' : asset_link_form})
    
    def handle_uploaded_file(self, f):
        with open('testfile.pdf', 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)

    def post(self, request):  
                  
        if request.POST.get("document_date"):   
            UserActivityLog().logUserActivity(request.user.username, "Document Create Completed")   
            ObjectCreate().documentObjectCreate(request)                              
            return self.get(request)
        
        elif request.POST.get("document_file_entry") :
            self.handle_uploaded_file(request.FILES['document_file_entry'])
            self.document_file_name = os.getcwd() + '/testfile.pdf'
            return HttpResponse(); 
        
        elif request.POST.get("document_type_id"):
            self.coordinate_result = SearchQuery().searchOCRCoordinatesByDocumentType(request.POST.get("document_type_id"))
            return HttpResponse();
            
        elif request.POST.get("document_type"):
            
            return SearchQuery().searchDocumentTypeByAutoComplete(request.POST.get("document_type"))
            
        elif self.request.POST.get("search_type"):
            attributeList = ['approval_agency', 'serial_number', 'tag_number']            
            return SearchQuery().searchAssetOrDocumentObjects(request, attributeList, 'asset_search')
    
    def runOCR(self):
        if self.coordinate_result and self.document_file_name: 
            ocrizer.input_file = open(self.document_file_name, 'rb')
            ocrizer.ocr_engine.process_and_download(ocrizer.post_file)
        

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
            flag = getUserType() 
            assetform = self.assetform_class(None)
            docform = self.docform_class(None)
            
            return render(request, self.template_name, {'assetform': assetform, 'docform' : docform, 'flag': flag})         
            
         
    def post(self, request):  
        if request.POST.get('search_type'):      
            if(request.POST.get('search_type') == 'asset_search'):     
                UserActivityLog().logUserActivity(request.user.username, "Asset Search")            
                attributeList = ['approval_agency', 'asset_type', 'status']                
                return SearchQuery().searchAssetOrDocumentObjects(request, attributeList, 'asset_search')
            
            else:                
                UserActivityLog().logUserActivity(request.user.username, "Document Search")  
                attributeList = ['document_type_id', 'document_date']                
                return SearchQuery().searchAssetOrDocumentObjects(request, attributeList, 'document_search')
        
        elif request.POST.get("document_type"):            
            return SearchQuery().searchDocumentTypeByAutoComplete(request.POST.get("document_type"))
        
        elif request.POST.get("event"):
            eventContent = request.POST.get("event")
            UserActivityLog().logUserActivity(request.user.username, eventContent)
            return HttpResponse(json.dumps("Event Success Logged"), content_type="application/json")
        
        else:            
            return HttpResponse(json.dumps("Error"), content_type="application/json")
              
@method_decorator(login_required, name='dispatch')
class DocDetail(DetailView):
    
    model = Document
    template_name = 'Documents/docDetail.html'
       
    def get(self, request, pk):
        
        return render(request, self.template_name, {'docFile' : self.get_object().document_file})
    
               
@method_decorator(login_required, name='dispatch')
class MainPage(View):      
    
    def get(self, request):
        flag = getUserType()
        return render(request, 'Documents/mainPage.html', {'flag' : flag})
        
    def post(self, request):
        
        eventType = request.POST.get('event')
        
        UserActivityLog().logUserActivity(request.user.username, eventType)   
        
        return redirect('Documents:main')
    
def logoutuser(request):

    UserActivityLog().logUserActivity(request.user.username, 'logout')
    
    logout(request)
      
    return redirect('Documents:login')

def error_page(request):
    
    return render(request, 'Documents/errorPage.html')

def getUserType():
    n = 10
    if n == 10:
        return "admin"
    else:
        return "user"

