from django.shortcuts import render
from .models import Asset, Document
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .form import AssetForm, DocForm



class IndexView(generic.ListView):
    template_name = 'Documents/index.html'
    context_object_name = 'all_assets'
    
    def get_queryset(self):
        return Asset.objects.all()

class DetailView(generic.DetailView):
    model = Asset
    template_name = 'Documents/detail.html'

class AssetCreate(CreateView):
    form_class = AssetForm
    template_name = 'Documents/assetCreate.html'

class DocCreate(CreateView):
    form_class = DocForm
    template_name = 'Documents/docCreate.html'

def login(request):       
    return render(request, 'Documents/loginPage.html')

def main(request):       
    return render(request, 'Documents/mainPage.html')

def search(request):       
    return render(request, 'Documents/search.html')

def assetEdit(request):       
    return render(request, 'Documents/assetEdit.html')

def docDetail(request):       
    return render(request, 'Documents/docDetail.html')

def docEdit(request):       
    return render(request, 'Documents/docEdit.html')
