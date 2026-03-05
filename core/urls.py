from django.urls import path
from .views import index, contato, produtos, clientes
from .views import salvarClientes, editaCliente, apagaCliente, entrar, sair
from .views import salvarProdutos, editarProdutos

urlpatterns = [
    path('', index, name="urlindex"),
    path('contato', contato, name="urlcontato"),
    path('produtos', produtos, name="urlprodutos"),
    path('clientes', clientes, name="urlclientes"),
    path('salvarClientes', salvarClientes, name="urlsalvarClientes"),
    path('editaCliente/<int:id>', editaCliente, name="urleditaCliente"),
    path('apagaCliente/<int:id>', apagaCliente, name="urlapagaCliente"),
    path('entrar', entrar, name="urlentrar"),
    path('sair', sair, name="urlsair"),
    path('salvarProdutos', salvarProdutos, name='urlsalvarProdutos'),
    path('editarProdutos/<int:id>', editarProdutos, name='urleditarProdutos'),
]