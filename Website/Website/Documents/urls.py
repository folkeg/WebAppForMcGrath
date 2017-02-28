from django.conf.urls import url
from . import views

app_name = 'Documents'

urlpatterns = [
    # Documents/
    url(r'^$', views.IndexView.as_view(), name='index'),
    # Documents/asset_id/
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    # Documents/main/assetCreate
    url(r'^asset/main/assetCreate/$', views.AssetCreate.as_view(), name='assetCreate'),
    # Documents/main/docCreate
    url(r'^asset/main/docCreate/$', views.DocCreate.as_view(), name='docCreate'),
    # Documents/login/
    url(r'^login/$', views.login, name='login'),
    # Documents/main/
    url(r'^main/$', views.main, name='main'),
    # Documents/main/search
    url(r'^main/search/$', views.search, name='search'),
    # Documents/main/search/assetsEdit
    url(r'^main/search/assetsEdit$', views.assetEdit, name='assetsEdit'),
    # Documents/main/search/docEdit
    url(r'^main/search/docEdit$', views.docEdit, name='docEdit'),
    # Documents/main/search/docDetail
    url(r'^main/search/docDetail$', views.docDetail, name='docDetail'),
]