from django.conf.urls import url
from . import views

app_name = 'Documents'

urlpatterns = [
    # Documents/main/search/assetEdit/
    url(r'^main/search/assetEdit/(?P<pk>[0-9]+)/$', views.AssetEditView.as_view(), name='assetEdit'),
    # Documents/main/search/documentEdit/
    url(r'^main/search/documentEdit/(?P<pk>[0-9]+)/$', views.DocumentEditView.as_view(), name='documentEdit'),
    # Documents/main/assetCreate
    url(r'^main/assetCreate/$', views.AssetCreate.as_view(), name='assetCreate'),
    # Documents/main/docCreate
    url(r'^main/docCreate/$', views.DocCreate.as_view(), name='docCreate'),
    # Documents/main/search
    url(r'^main/search/$', views.Search.as_view(), name='search'),
    # Documents/login/
    url(r'^login/$', views.UserFormView.as_view(), name='login'),
    # Documents/logoutuser/
    url(r'^logoutuser/$', views.logoutuser, name='logout'),
    # Documents/main/
    url(r'^main/$', views.main, name='main'),
    # Documents/main/search/docDetail
    url(r'^main/search/docDetail$', views.docDetail, name='docDetail'),
]