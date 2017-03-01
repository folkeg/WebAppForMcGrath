from django.shortcuts import render
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import View
from .form import AssetForm, DocForm, UserForm
from .models import Asset, Document
from aetypes import template

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
                  
        user = authenticate(username = username, password = password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('Documents:main')
        
        login_invalid = 'login is invalid, username or password is wrong'
        return render(request, self.template_name, {'form': form, 'error_message' :login_invalid})


class AssetCreate(CreateView):
    form_class = AssetForm
    template_name = 'Documents/assetCreate.html'
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(AssetCreate, self).dispatch(*args, **kwargs)
    
@method_decorator(login_required, name='dispatch')
class DocCreate(CreateView):
    form_class = DocForm
    template_name = 'Documents/docCreate.html'

@login_required(login_url='Documents:login')
def main(request):       
    return render(request, 'Documents/mainPage.html')

@method_decorator(login_required, name='dispatch')
def search(request):       
    return render(request, 'Documents/search.html')

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
