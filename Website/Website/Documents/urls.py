from django.conf.urls import url
from . import views

app_name = 'Documents'

urlpatterns = [
    # Documents/
    url(r'^$', views.IndexView.as_view(), name='index'),
    # Documents/asset_id/
    url(r'^(?P<pk>[0-9]+)/$', views.AssetDetailView.as_view(), name='assetDetail'),
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
    # Documents/main/search/assetsEdit
    url(r'^main/search/assetsEdit$', views.assetEdit, name='assetsEdit'),
    # Documents/main/search/docEdit
    url(r'^main/search/docEdit$', views.docEdit, name='docEdit'),
    # Documents/main/search/docDetail
    url(r'^main/search/docDetail$', views.docDetail, name='docDetail'),
]