from django.urls import path
from .views import index, contato, produtos, clientes
from .views import cadastraClientes, salvarClientes


urlpatterns = [
    path('', index, name="urlindex"),
    path('contato', contato, name="urlcontato"),
    path('produtos', produtos, name="urlprodutos"),
    path('clientes', clientes, name="urlclientes"),
    path('cadastraClientes', cadastraClientes, name="urlcadastraClientes"),
    path('salvarClientes', salvarClientes, name="urlsalvarClientes"),
]