from django.conf.urls import url
from . import views
from .models import *

app_name = 'mailAdmin'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(model=Domain), name='domainIndex'),
    url(r'^login/', views.LoginView.as_view(), name='login'),
    url(r'^logout/', views.LogoutView.as_view(), name='logout'),
    url(r'^new/$', views.NewView.as_view(model=Domain), name='domainNew'),
    url(r'^(?P<domain>[\w\d\-\.]+\.[\w\d\-\.]{2,})/$', views.EditView.as_view(model=Domain), name='domainEdit'),
    url(r'^(?P<domain>[\w\d\-\.]+\.[\w\d\-\.]{2,})/delete/$', views.DeleteView.as_view(model=Domain), name='domainDelete'),
    url(r'^(?P<domain>[\w\d\-\.]+\.[\w\d\-\.]{2,})/accounts/$', views.IndexView.as_view(model=Account), name='domainAccounts'),
    url(r'^(?P<domain>[\w\d\-\.]+\.[\w\d\-\.]{2,})/accounts/new/$', views.NewView.as_view(model=Account), name='accountNew'),
    url(r'^(?P<domain>[\w\d\-\.]+\.[\w\d\-\.]{2,})/accounts/(?P<account>[\w\d\-\.]+)/$', views.EditView.as_view(model=Account), name='accountEdit'),
    url(r'^(?P<domain>[\w\d\-\.]+\.[\w\d\-\.]{2,})/accounts/(?P<account>[\w\d\-\.]+)/delete/$', views.DeleteView.as_view(model=Account), name='accountDelete'),
    url(r'^(?P<domain>[\w\d\-\.]+\.[\w\d\-\.]{2,})/accounts/(?P<account>[\w\d\-\.]+)/aliases/$', views.SubModelIndexView.as_view(model=Account, sub_model=Alias), name='accountAliases'),
    url(r'^(?P<domain>[\w\d\-\.]+\.[\w\d\-\.]{2,})/accounts/(?P<account>[\w\d\-\.]+)/aliases/add/$', views.SubModelAddView.as_view(model=Account, sub_model=Alias), name='accountAliasAdd'),
    url(r'^(?P<domain>[\w\d\-\.]+\.[\w\d\-\.]{2,})/accounts/(?P<account>[\w\d\-\.]+)/aliases/(?P<alias>\d+)/remove/$', views.SubModelRemoveView.as_view(model=Account, sub_model=Alias), name='accountAliasRemove'),
    url(r'^(?P<domain>[\w\d\-\.]+\.[\w\d\-\.]{2,})/accounts/(?P<account>[\w\d\-\.]+)/lists/$', views.SubModelIndexView.as_view(model=Account, sub_model=Mailinglist), name='accountMailinglists'),
    url(r'^(?P<domain>[\w\d\-\.]+\.[\w\d\-\.]{2,})/accounts/(?P<account>[\w\d\-\.]+)/lists/add/$', views.SubModelAddView.as_view(model=Account, sub_model=Mailinglist), name='accountMailinglistAdd'),
    url(r'^(?P<domain>[\w\d\-\.]+\.[\w\d\-\.]{2,})/accounts/(?P<account>[\w\d\-\.]+)/lists/(?P<mailing_list>\d+)/remove/$', views.SubModelRemoveView.as_view(model=Account, sub_model=Mailinglist), name='accountMailinglistRemove'),
    url(r'^(?P<domain>[\w\d\-\.]+\.[\w\d\-\.]{2,})/aliases/$', views.IndexView.as_view(model=Alias), name='domainAliases'),
    url(r'^(?P<domain>[\w\d\-\.]+\.[\w\d\-\.]{2,})/aliases/new/$', views.NewView.as_view(model=Alias), name='aliasNew'),
    url(r'^(?P<domain>[\w\d\-\.]+\.[\w\d\-\.]{2,})/aliases/(?P<alias>[\w\d\-\.]+)/delete/$', views.DeleteView.as_view(model=Alias), name='aliasDelete'),
    url(r'^(?P<domain>[\w\d\-\.]+\.[\w\d\-\.]{2,})/lists/$', views.IndexView.as_view(model=Mailinglist), name='domainLists'),
    url(r'^(?P<domain>[\w\d\-\.]+\.[\w\d\-\.]{2,})/lists/new/$', views.NewView.as_view(model=Mailinglist), name='mailinglistNew'),
    url(r'^(?P<domain>[\w\d\-\.]+\.[\w\d\-\.]{2,})/lists/(?P<list>[\w\d\-\.]+)/delete/$', views.DeleteView.as_view(model=Mailinglist), name='mailinglistDelete'),
    url(r'^(?P<domain>[\w\d\-\.]+\.[\w\d\-\.]{2,})/lists/(?P<list>[\w\d\-\.]+)/accounts/$', views.SubModelIndexView.as_view(model=Mailinglist, sub_model=Account), name='mailinglistAccounts'),
    url(r'^(?P<domain>[\w\d\-\.]+\.[\w\d\-\.]{2,})/lists/(?P<list>[\w\d\-\.]+)/accounts/add/$', views.SubModelAddView.as_view(model=Mailinglist, sub_model=Account), name='mailinglistAccountAdd'),
    url(r'^(?P<domain>[\w\d\-\.]+\.[\w\d\-\.]{2,})/lists/(?P<list>[\w\d\-\.]+)/accounts/(?P<account>\d+)/delete/$', views.SubModelRemoveView.as_view(model=Mailinglist, sub_model=Account), name='mailinglistAccountRemove'),
    url(r'^(?P<domain>[\w\d\-\.]+\.[\w\d\-\.]{2,})/lists/(?P<list>[\w\d\-\.]+)/externals/$', views.SubModelIndexView.as_view(model=Mailinglist, sub_model=ExternalReceiver), name='mailinglistExternals'),
    url(r'^(?P<domain>[\w\d\-\.]+\.[\w\d\-\.]{2,})/lists/(?P<list>[\w\d\-\.]+)/externals/add/$', views.SubModelAddView.as_view(model=Mailinglist, sub_model=ExternalReceiver), name='mailinglistExternalAdd'),
    url(r'^(?P<domain>[\w\d\-\.]+\.[\w\d\-\.]{2,})/lists/(?P<list>[\w\d\-\.]+)/externals/(?P<external_receiver>\d+)/delete/$', views.SubModelRemoveView.as_view(model=Mailinglist, sub_model=ExternalReceiver), name='mailinglistExternalRemove'),
    url(r'^(?P<domain>[\w\d\-\.]+\.[\w\d\-\.]{2,})/redirects/$', views.IndexView.as_view(model=Redirect), name='domainRedirects'),
    url(r'^(?P<domain>[\w\d\-\.]+\.[\w\d\-\.]{2,})/redirects/new/$', views.NewView.as_view(model=Redirect), name='redirectNew'),
    url(r'^(?P<domain>[\w\d\-\.]+\.[\w\d\-\.]{2,})/redirects/(?P<redirect>[\w\d\-\.]+)/delete/$', views.DeleteView.as_view(model=Redirect), name='redirectDelete'),
]
