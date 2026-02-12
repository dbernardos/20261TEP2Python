from django.urls import path
from .views import index, contato, produtos

urlpatterns = [
    path('', index, name="urlindex"),
    path('contato', contato, name="urlcontato"),
    path('produtos', produtos, name="urlprodutos"),
]